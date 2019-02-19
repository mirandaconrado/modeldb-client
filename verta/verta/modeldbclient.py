from typing import Any, Union, Tuple

import re
import ast
import time
import json

from google.protobuf import json_format
import requests

from .protos.modeldb import CommonService_pb2
from .protos.modeldb import ExperimentService_pb2
from .protos.modeldb import ProjectService_pb2
from .protos.modeldb import ExperimentRunService_pb2


class ModelDBClient:
    GRPC_PREFIX = "Grpc-Metadata-"
    SOURCE = "PythonClient"

    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = "8080"

    def __init__(self, email, dev_key, source=SOURCE, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self._auth = {self.GRPC_PREFIX+'email': email,
                      self.GRPC_PREFIX+'developer_key': dev_key,
                      self.GRPC_PREFIX+'source': source}

        self._socket = "{}:{}".format(host, port)

        self.proj = None
        self.expt = None

    @property
    def expt_runs(self):
        if self.expt is None:
            return None
        else:
            msg = ExperimentRunService_pb2.GetExperimentRunsInProject(project_id=self.proj._id)
            data = json.loads(json_format.MessageToJson(msg,
                                                        preserving_proto_field_name=True,
                                                        use_integers_for_enums=True))
            response = requests.get("http://{}/v1/experiment-run/getExperimentRunsInProject".format(self._socket),
                                    params=data, headers=self._auth)
            if response.ok:
                expt_run_ids = [expt_run['id']
                                for expt_run in response.json().get('experiment_runs', [])
                                if expt_run['experiment_id'] == self.expt._id]
                return ExperimentRuns(self._auth, self._socket, expt_run_ids)
            else:
                raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

    def set_project(self, proj_name=None):
        # if proj already in progress, reset expt
        if self.proj is not None:
            self.expt = None

        proj = Project(self._auth, self._socket, proj_name)

        self.proj = proj
        return proj

    def set_experiment(self, expt_name=None):
        if self.proj is None:
            raise AttributeError("a project must first in progress")

        expt = Experiment(self._auth, self._socket, self.proj._id, expt_name)

        self.expt = expt
        return expt

    def set_experiment_run(self, expt_run_name=None):
        if self.expt is None:
            raise AttributeError("an experiment must first in progress")

        return ExperimentRun(self._auth, self._socket,
                             self.proj._id, self.expt._id,
                             expt_run_name)


class Project:
    def __init__(self, auth, socket, proj_name=None, *, _proj_id=None):
        if proj_name is not None and _proj_id is not None:
            raise ValueError("cannot specify both `proj_name` and `_proj_id`")

        if _proj_id is not None:
            proj = Project._get(auth, socket, _proj_id=_proj_id)
            if proj is not None:
                print("set existing Project: {}".format(proj['name']))
            else:
                raise ValueError("Project with ID {} not found".format(_proj_id))
        else:
            if proj_name is None:
                proj_name = Project._generate_default_name()
            proj = Project._get(auth, socket, proj_name)
            if proj is not None:
                print("set existing Project: {}".format(proj['name']))
            else:
                proj = Project._create(auth, socket, proj_name)
                print("created new Project: {}".format(proj['name']))

        self._auth = auth
        self._socket = socket
        self._id = proj['id']

    @property
    def name(self):
        msg = ProjectService_pb2.GetProjectById(id=self._id)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.get("http://{}/v1/project/getProjectById".format(self._socket),
                                params=data, headers=self._auth)
        if response.ok:
            return response.json().get('name', [])
        else:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

    @staticmethod
    def _generate_default_name():
        return "Project {}".format(int(time.time()))

    @staticmethod
    def _get(auth, socket, proj_name=None, *, _proj_id=None):
        if _proj_id is not None:
            msg = ProjectService_pb2.GetProjectById(id=_proj_id)
            data = json.loads(json_format.MessageToJson(msg,
                                                        preserving_proto_field_name=True,
                                                        use_integers_for_enums=True))
            response = requests.get("http://{}/v1/project/getProjectById".format(socket),
                                    params=data, headers=auth)
        elif proj_name is not None:
            msg = ProjectService_pb2.GetProjectByName(name=proj_name)
            data = json.loads(json_format.MessageToJson(msg,
                                                        preserving_proto_field_name=True,
                                                        use_integers_for_enums=True))
            response = requests.get("http://{}/v1/project/getProjectByName".format(socket),
                                    params=data, headers=auth)
        else:
            raise ValueError("insufficient arguments")

        if response.ok:
            return response.json().get('project', [])[0]  # becasue of collaboration
        else:
            if ((response.status_code == 401 and response.json()['code'] == 16)
                    or (response.status_code == 404 and response.json()['code'] == 5)):
                return None
            else:
                raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

    @staticmethod
    def _create(auth, socket, proj_name):
        msg = ProjectService_pb2.CreateProject(name=proj_name)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.post("http://{}/v1/project/createProject".format(socket),
                                 json=data, headers=auth)

        if response.ok:
            return response.json().get('project', [])
        else:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

    def find(self, where, ret_all_info=False):
        expt_runs = ExperimentRuns(self._auth, self._socket)
        return expt_runs.find(where, ret_all_info, _proj_id=self._id)

    def top_k(self, key, k, ret_all_info=False):
        expt_runs = ExperimentRuns(self._auth, self._socket)
        return expt_runs._top_k(key, k, ret_all_info, _proj_id=self._id)

    def bottom_k(self, key, k, ret_all_info=False):
        expt_runs = ExperimentRuns(self._auth, self._socket)
        return expt_runs._bottom_k(key, k, ret_all_info, _proj_id=self._id)


class Experiment:
    def __init__(self, auth, socket, proj_id=None, expt_name=None, *, _expt_id=None):
        if expt_name is not None and _expt_id is not None:
            raise ValueError("cannot specify both `expt_name` and `_expt_id`")

        if _expt_id is not None:
            expt = Experiment._get(auth, socket, _expt_id=_expt_id)
            if expt is not None:
                print("set existing Experiment: {}".format(expt['name']))
            else:
                raise ValueError("Experiment with ID {} not found".format(_expt_id))
        elif proj_id is not None:
            if expt_name is None:
                expt_name = Experiment._generate_default_name()
            expt = Experiment._get(auth, socket, proj_id, expt_name)
            if expt is not None:
                print("set existing Experiment: {}".format(expt['name']))
            else:
                expt = Experiment._create(auth, socket, proj_id, expt_name)
                print("created new Experiment: {}".format(expt['name']))
        else:
            raise ValueError("insufficient arguments")

        self._auth = auth
        self._socket = socket
        self._id = expt['id']

    @property
    def name(self):
        msg = ExperimentService_pb2.GetExperimentById(id=self._id)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.get("http://{}/v1/experiment/getExperimentById".format(self._socket),
                                params=data, headers=self._auth)
        if response.ok:
            return response.json().get('name', [])
        else:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

    @staticmethod
    def _generate_default_name():
        return "Experiment {}".format(int(time.time()))

    @staticmethod
    def _get(auth, socket, proj_id=None, expt_name=None, *, _expt_id=None):
        if _expt_id is not None:
            msg = ExperimentService_pb2.GetExperimentById(id=_expt_id)
            data = json.loads(json_format.MessageToJson(msg,
                                                        preserving_proto_field_name=True,
                                                        use_integers_for_enums=True))
            response = requests.get("http://{}/v1/experiment/getExperimentById".format(socket),
                                    params=data, headers=auth)
        elif None not in (proj_id, expt_name):
            msg = ExperimentService_pb2.GetExperimentByName(project_id=proj_id, name=expt_name)
            data = json.loads(json_format.MessageToJson(msg,
                                                        preserving_proto_field_name=True,
                                                        use_integers_for_enums=True))
            response = requests.get("http://{}/v1/experiment/getExperimentByName".format(socket),
                                    params=data, headers=auth)
        else:
            raise ValueError("insufficient arguments")

        if response.ok:
            return response.json().get('experiment', [])
        else:
            if ((response.status_code == 401 and response.json()['code'] == 16)
                    or (response.status_code == 404 and response.json()['code'] == 5)):
                return None
            else:
                raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

    @staticmethod
    def _create(auth, socket, proj_id, expt_name):
        msg = ExperimentService_pb2.CreateExperiment(project_id=proj_id, name=expt_name)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.post("http://{}/v1/experiment/createExperiment".format(socket),
                                 json=data, headers=auth)

        if response.ok:
            return response.json().get('experiment', [])
        else:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

    def find(self, where, ret_all_info=False):
        expt_runs = ExperimentRuns(self._auth, self._socket)
        return expt_runs.find(where, ret_all_info, _expt_id=self._id)

    def top_k(self, key, k, ret_all_info=False):
        expt_runs = ExperimentRuns(self._auth, self._socket)
        return expt_runs._top_k(key, k, ret_all_info, _expt_id=self._id)

    def bottom_k(self, key, k, ret_all_info=False):
        expt_runs = ExperimentRuns(self._auth, self._socket)
        return expt_runs._bottom_k(key, k, ret_all_info, _expt_id=self._id)


class ExperimentRuns:
    _OP_MAP = {'==': ExperimentRunService_pb2.OperatorEnum.EQ,
               '!=': ExperimentRunService_pb2.OperatorEnum.NE,
               '>':  ExperimentRunService_pb2.OperatorEnum.GT,
               '>=': ExperimentRunService_pb2.OperatorEnum.GTE,
               '<':  ExperimentRunService_pb2.OperatorEnum.LT,
               '<=': ExperimentRunService_pb2.OperatorEnum.LTE}
    _OP_PATTERN = re.compile(r"({})".format('|'.join(sorted(_OP_MAP.keys(), key=lambda s: len(s), reverse=True))))

    def __init__(self, auth, socket, expt_run_ids=None):
        self._auth = auth
        self._socket = socket
        self._ids = expt_run_ids if expt_run_ids is not None else []

    def __getitem__(self, key):
        if isinstance(key, int):
            expt_run_id = self._ids[key]
            return ExperimentRun(self._auth, self._socket, _expt_run_id=expt_run_id)
        elif isinstance(key, slice):
            expt_run_ids = self._ids[key]
            return self.__class__(self._auth, self._socket, expt_run_ids)
        else:
            raise TypeError("index must be integer or slice, not {}".format(type(key)))

    def __len__(self):
        return len(self._ids)

    def find(self, where, ret_all_info=False, *, _proj_id=None, _expt_id=None):
        if _proj_id is not None and _expt_id is not None:
            raise ValueError("cannot specify both `_proj_id` and `_expt_id`")
        elif _proj_id is None and _expt_id is None:
            if len(self._ids) == 0:
                raise ValueError("insufficient arguments")
            else:
                expt_run_ids = self._ids
        else:
            expt_run_ids = None

        predicates = []
        for predicate in where:
            # split predicate
            try:
                key, operator, value = map(str.strip, self._OP_PATTERN.split(predicate, maxsplit=1))
            except ValueError:
                raise ValueError("predicate `{}` must be a two-operand comparison".format(predicate))

            # cast operator into protobuf enum variant
            operator = self._OP_MAP[operator]

            # parse value
            try:
                expr_node = ast.parse(value, mode='eval')
            except SyntaxError:
                raise ValueError("value `{}` must be a number or string literal".format(value))
            value_node = expr_node.body
            if type(value_node) is ast.Num:
                value = value_node.n
            elif type(value_node) is ast.Str:
                value = value_node.s
            elif type(value_node) is ast.Compare:
                raise ValueError("predicate `{}` must be a two-operand comparison".format(predicate))
            else:
                raise ValueError("value `{}` must be a number or string literal".format(value))
            proto_type = _get_proto_type(value)

            predicates.append(ExperimentRunService_pb2.KeyValueQuery(key=key, value=str(value),
                                                                     value_type=proto_type,
                                                                     operator=operator))
        msg = ExperimentRunService_pb2.FindExperimentRuns(project_id=_proj_id,
                                                          experiment_id=_expt_id,
                                                          experiment_run_ids=expt_run_ids,
                                                          predicates=predicates,
                                                          ids_only=not ret_all_info)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.post("http://{}/v1/experiment-run/findExperimentRuns".format(self._socket),
                                 json=data, headers=self._auth)
        if response.ok:
            if ret_all_info:
                return response.json().get('experiment_runs', [])
            else:
                return self.__class__(self._auth, self._socket,
                                      [expt_run['id'] for expt_run in response.json().get('experiment_runs', [])])
        else:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

    def sort(self, key, descending=False, ret_all_info=False):
        msg = ExperimentRunService_pb2.SortExperimentRuns(experiment_run_ids=self._ids,
                                                          sort_key=key,
                                                          ascending=not descending,
                                                          ids_only=not ret_all_info)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.get("http://{}/v1/experiment-run/sortExperimentRuns".format(self._socket),
                                params=data, headers=self._auth)
        if response.ok:
            if ret_all_info:
                return response.json().get('experiment_runs', [])
            else:
                return self.__class__(self._auth, self._socket,
                                      [expt_run['id'] for expt_run in response.json().get('experiment_runs', [])])
        else:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

    def _top_k(self, key, k, ret_all_info=False, *, _proj_id=None, _expt_id=None):
        if _proj_id is not None and _expt_id is not None:
            raise ValueError("cannot specify both `_proj_id` and `_expt_id`")
        if _proj_id is None and _expt_id is None:
            raise ValueError("must specify either `_proj_id` and `_expt_id`")

        raise NotImplementedError()
        msg = ExperimentRunService_pb2.TopExperimentRunsSelector(project_id=_proj_id,
                                                                 experiment_id=_expt_id,
                                                                 sort_key=key,
                                                                 ascending=False,
                                                                 top_k=k)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.get("http://{}/v1/experiment-run/getTopExperimentRuns".format(self._socket),
                                params=data, headers=self._auth)
        if response.ok:
            if ret_all_info:
                return response.json().get('experiment_runs', [])
            else:
                return self.__class__(self._auth, self._socket,
                                      [expt_run['id'] for expt_run in response.json().get('experiment_runs', [])])
        else:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

    def _bottom_k(self, key, k, ret_all_info=False, *, _proj_id=None, _expt_id=None):
        if _proj_id is not None and _expt_id is not None:
            raise ValueError("cannot specify both `_proj_id` and `_expt_id`")
        if _proj_id is None and _expt_id is None:
            raise ValueError("must specify either `_proj_id` and `_expt_id`")

        raise NotImplementedError()
        msg = ExperimentRunService_pb2.TopExperimentRunsSelector(project_id=_proj_id,
                                                                 experiment_id=_expt_id,
                                                                 sort_key=key,
                                                                 ascending=True,
                                                                 top_k=k)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.get("http://{}/v1/experiment-run/getTopExperimentRuns".format(self._socket),
                                params=data, headers=self._auth)
        if response.ok:
            if ret_all_info:
                return response.json().get('experiment_runs', [])
            else:
                return self.__class__(self._auth, self._socket,
                                      [expt_run['id'] for expt_run in response.json().get('experiment_runs', [])])
        else:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))


class ExperimentRun:
    def __init__(self, auth, socket, proj_id=None, expt_id=None, expt_run_name=None, *, _expt_run_id=None):
        if expt_run_name is not None and _expt_run_id is not None:
            raise ValueError("cannot specify both `expt_run_name` and `_expt_run_id`")

        if _expt_run_id is not None:
            expt_run = ExperimentRun._get(auth, socket, _expt_run_id=_expt_run_id)
            if expt_run is not None:
                pass
            else:
                raise ValueError("ExperimentRun with ID {} not found".format(_expt_run_id))
        elif None not in (proj_id, expt_id):
            if expt_run_name is None:
                expt_run_name = ExperimentRun._generate_default_name()
            expt_run = ExperimentRun._get(auth, socket, proj_id, expt_id, expt_run_name)
            if expt_run is not None:
                pass
            else:
                expt_run = ExperimentRun._create(auth, socket, proj_id, expt_id, expt_run_name)
        else:
            raise ValueError("insufficient arguments")

        self._auth = auth
        self._socket = socket
        self._id = expt_run['id']

    @property
    def name(self):
        msg = ExperimentRunService_pb2.GetExperimentRunById(id=self._id)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.get("http://{}/v1/experiment-run/getExperimentRunById".format(self._socket),
                                params=data, headers=self._auth)
        if response.ok:
            return response.json().get('name', [])
        else:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

    @staticmethod
    def _generate_default_name():
        return "ExperimentRun {}".format(int(time.time()))

    @staticmethod
    def _get(auth, socket, proj_id=None, expt_id=None, expt_run_name=None, *, _expt_run_id=None):
        if _expt_run_id is not None:
            msg = ExperimentRunService_pb2.GetExperimentRunById(id=_expt_run_id)
            data = json.loads(json_format.MessageToJson(msg,
                                                        preserving_proto_field_name=True,
                                                        use_integers_for_enums=True))
            response = requests.get("http://{}/v1/experiment-run/getExperimentRunById".format(socket),
                                    params=data, headers=auth)
        elif None not in (proj_id, expt_id, expt_run_name):
            # TODO: swap blocks when RPC is implemented
            # msg = ExperimentRunService_pb2.GetExperimentByName(project_id=proj_id, experiment_id=expt_id, name=expt_name)
            # data = json.loads(json_format.MessageToJson(msg,
            #                                             preserving_proto_field_name=True,
            #                                             use_integers_for_enums=True))
            # response = requests.post("http://{}/v1/experiment-run/getExperimentRunByName".format(socket),
            #                          json=data, headers=self._auth)
            msg = ExperimentRunService_pb2.GetExperimentRunsInProject(project_id=proj_id)
            data = json.loads(json_format.MessageToJson(msg,
                                                        preserving_proto_field_name=True,
                                                        use_integers_for_enums=True))
            response = requests.get("http://{}/v1/experiment-run/getExperimentRunsInProject".format(socket),
                                    params=data, headers=auth)
            if not response.ok:
                raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))
            else:
                if 'experiment_runs' in response.json():
                    result = [expt_run for expt_run in response.json().get('experiment_runs', []) if expt_run['name'] == expt_run_name]
                    return result[-1] if len(result) else None
                else:  # no expt_runs in proj
                    return None
        else:
            raise ValueError("insufficient arguments")

        if response.ok:
            return response.json().get('experiment_run', [])
        else:
            if ((response.status_code == 401 and response.json()['code'] == 16)
                    or (response.status_code == 404 and response.json()['code'] == 5)):
                return None
            else:
                raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

    @staticmethod
    def _create(auth, socket, proj_id, expt_id, expt_run_name):
        msg = ExperimentRunService_pb2.CreateExperimentRun(project_id=proj_id, experiment_id=expt_id, name=expt_run_name)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.post("http://{}/v1/experiment-run/createExperimentRun".format(socket),
                                 json=data, headers=auth)

        if response.ok:
            return response.json().get('experiment_run', [])
        else:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

    def log_attribute(self, name, value):
        proto_type = _get_proto_type(value)
        attribute = CommonService_pb2.KeyValue(key=name, value=str(value),
                                               value_type=proto_type)
        msg = ExperimentRunService_pb2.LogAttribute(id=self._id,
                                                    attribute=attribute)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.post("http://{}/v1/experiment-run/logAttribute".format(self._socket),
                                 json=data, headers=self._auth)
        if not response.ok:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

    def get_attributes(self):
        msg = ExperimentRunService_pb2.GetAttributes(id=self._id)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.get("http://{}/v1/experiment-run/getAttributes".format(self._socket),
                                params=data, headers=self._auth)
        if not response.ok:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

        return {attribute['key']: _cast_to_python(attribute['value'], attribute.get('value_type', "STRING"))
                for attribute in response.json().get('attributes', [])}

    def log_metric(self, name, value):
        proto_type = _get_proto_type(value)
        metric = CommonService_pb2.KeyValue(key=name, value=str(value),
                                            value_type=proto_type)
        msg = ExperimentRunService_pb2.LogMetric(id=self._id,
                                                 metric=metric)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.post("http://{}/v1/experiment-run/logMetric".format(self._socket),
                                 json=data, headers=self._auth)
        if not response.ok:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

    def get_metrics(self):
        msg = ExperimentRunService_pb2.GetMetrics(id=self._id)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.get("http://{}/v1/experiment-run/getMetrics".format(self._socket),
                                params=data, headers=self._auth)
        if not response.ok:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

        return {metric['key']: _cast_to_python(metric['value'], metric.get('value_type', "STRING"))
                for metric in response.json().get('metrics', [])}

    def log_hyperparameter(self, name, value):
        proto_type = _get_proto_type(value)
        hyperparameter = CommonService_pb2.KeyValue(key=name, value=str(value),
                                                    value_type=proto_type)
        msg = ExperimentRunService_pb2.LogHyperparameter(id=self._id,
                                                         hyperparameter=hyperparameter)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.post("http://{}/v1/experiment-run/logHyperparameter".format(self._socket),
                                 json=data, headers=self._auth)
        if not response.ok:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

    def get_hyperparameters(self):
        msg = ExperimentRunService_pb2.GetHyperparameters(id=self._id)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.get("http://{}/v1/experiment-run/getHyperparameters".format(self._socket),
                                params=data, headers=self._auth)
        if not response.ok:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

        return {hyperparameter['key']: _cast_to_python(hyperparameter['value'], hyperparameter.get('value_type', "STRING"))
                for hyperparameter in response.json().get('hyperparameters', [])}

    def log_dataset(self, name, path):
        dataset = CommonService_pb2.Artifact(key=name, path=path,
                                             artifact_type=CommonService_pb2.ArtifactTypeEnum.DATA)
        msg = ExperimentRunService_pb2.LogDataset(id=self._id,
                                                  dataset=dataset)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.post("http://{}/v1/experiment-run/logDataset".format(self._socket),
                                 json=data, headers=self._auth)
        if not response.ok:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

    def get_datasets(self):
        msg = ExperimentRunService_pb2.GetDatasets(id=self._id)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.get("http://{}/v1/experiment-run/getDatasets".format(self._socket),
                                params=data, headers=self._auth)
        if not response.ok:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

        return {dataset['key']: dataset['path'] for dataset in response.json().get('datasets', [])}

    def log_model(self, name, path):
        model = CommonService_pb2.Artifact(key=name, path=path,
                                           artifact_type=CommonService_pb2.ArtifactTypeEnum.MODEL)
        msg = ExperimentRunService_pb2.LogArtifact(id=self._id,
                                                   artifact=model)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.post("http://{}/v1/experiment-run/logArtifact".format(self._socket),
                                 json=data, headers=self._auth)
        if not response.ok:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

    def get_models(self):
        msg = ExperimentRunService_pb2.GetArtifacts(id=self._id)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.get("http://{}/v1/experiment-run/getArtifacts".format(self._socket),
                                params=data, headers=self._auth)
        if not response.ok:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

        return {artifact['key']: artifact['path']
                for artifact in response.json().get('artifacts', [])
                if artifact.get('artifact_type', "IMAGE") == "MODEL"}

    def log_image(self, name, path):
        image = CommonService_pb2.Artifact(key=name, path=path,
                                           artifact_type=CommonService_pb2.ArtifactTypeEnum.IMAGE)
        msg = ExperimentRunService_pb2.LogArtifact(id=self._id,
                                                   artifact=image)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.post("http://{}/v1/experiment-run/logArtifact".format(self._socket),
                                 json=data, headers=self._auth)
        if not response.ok:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

    def get_image(self, name):  # TODO: this, but better
        msg = ExperimentRunService_pb2.GetArtifacts(id=self._id)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.get("http://{}/v1/experiment-run/getArtifacts".format(self._socket),
                                params=data, headers=self._auth)
        if not response.ok:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

        return [artifact['path']
                for artifact in response.json().get('artifacts', [])
                if artifact.get('artifact_type', "IMAGE") == "IMAGE"
                and artifact['key'] == name][0]

    def log_observation(self, name, value):
        proto_type = _get_proto_type(value)
        attribute = CommonService_pb2.KeyValue(key=name, value=str(value),
                                               value_type=proto_type)
        observation = ExperimentRunService_pb2.Observation(attribute=attribute)  # TODO: support Artifacts
        msg = ExperimentRunService_pb2.LogObservation(id=self._id,
                                                      observation=observation)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.post("http://{}/v1/experiment-run/logObservation".format(self._socket),
                                 json=data, headers=self._auth)
        if not response.ok:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

    def get_observations(self, name):
        msg = ExperimentRunService_pb2.GetObservations(id=self._id,
                                                       observation_key=name)
        data = json.loads(json_format.MessageToJson(msg,
                                                    preserving_proto_field_name=True,
                                                    use_integers_for_enums=True))
        response = requests.get("http://{}/v1/experiment-run/getObservations".format(self._socket),
                                params=data, headers=self._auth)
        if not response.ok:
            raise requests.HTTPError("{}: {}".format(response.status_code, response.reason))

        return [_cast_to_python(observation['attribute']['value'], observation['attribute'].get('value_type', "STRING"))
                for observation in response.json().get('observations', [])]  # TODO: support Artifacts


def _get_proto_type(val):
    if isinstance(val, float) or isinstance(val, int):
        return CommonService_pb2.ValueTypeEnum.NUMBER
    else:
        return CommonService_pb2.ValueTypeEnum.STRING


def _cast_to_python(val, proto_type):
    if proto_type == "NUMBER":
        try:
            return int(val)
        except ValueError:
            return float(val)
    else:
        return str(val)