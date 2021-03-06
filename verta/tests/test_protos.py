import pytest

import requests


class TestGetChildren:
    def test_get_experiments_in_project(self, client):
        expt_ids = []

        proj = client.set_project()
        for _ in range(4):
            expt_ids.append(client.set_experiment()._id)

        response = requests.get("http://{}/v1/experiment/getExperimentsInProject".format(client._socket),
                                params={'project_id': proj._id}, headers=client._auth)
        response.raise_for_status()
        assert set(expt_ids) == set(experiment['id'] for experiment in response.json()['experiments'])

    def test_get_experiment_runs_in_project(self, client):
        run_ids = []

        proj = client.set_project()
        expt = client.set_experiment()
        for _ in range(4):
            run_ids.append(client.set_experiment_run()._id)
        expt = client.set_experiment()
        for _ in range(4):
            run_ids.append(client.set_experiment_run()._id)

        response = requests.get("http://{}/v1/experiment-run/getExperimentRunsInProject".format(client._socket),
                                params={'project_id': proj._id}, headers=client._auth)
        response.raise_for_status()
        assert set(run_ids) == set(experiment_run['id'] for experiment_run in response.json()['experiment_runs'])

    def test_get_experiment_runs_in_experiment(self, client):
        run_ids = []

        proj = client.set_project()
        expt = client.set_experiment()
        for _ in range(4):
            run_ids.append(client.set_experiment_run()._id)

        response = requests.get("http://{}/v1/experiment-run/getExperimentRunsInExperiment".format(client._socket),
                                params={'experiment_id': expt._id}, headers=client._auth)
        response.raise_for_status()
        assert set(run_ids) == set(experiment_run['id'] for experiment_run in response.json()['experiment_runs'])
