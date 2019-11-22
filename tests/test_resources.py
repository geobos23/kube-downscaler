from unittest.mock import MagicMock

from pykube.objects import NamespacedAPIObject

from pykube import Deployment, StatefulSet, DaemonSet
from kube_downscaler.resources.stack import Stack


def test_deployment():
    api_mock = MagicMock(spec=NamespacedAPIObject, name="APIMock")
    scalable_mock = {'spec': {'replicas': 3}}
    api_mock.obj = MagicMock(name="APIObjMock")
    d = Deployment(api_mock, scalable_mock)
    r = d.replicas
    assert r == 3
    d.replicas = 10
    assert scalable_mock['spec']['replicas'] == 10


def test_statefulset():
    api_mock = MagicMock(spec=NamespacedAPIObject, name="APIMock")
    scalable_mock = {'spec': {'replicas': 3}}
    api_mock.obj = MagicMock(name="APIObjMock")
    d = StatefulSet(api_mock, scalable_mock)
    r = d.replicas
    assert r == 3
    d.replicas = 10
    assert scalable_mock['spec']['replicas'] == 10


def test_daemonset_scale_up():
    api_mock = MagicMock(spec=NamespacedAPIObject, name="APIMock")
    scalable_mock = {'spec': {'nodeSelector': {'non-existing': 'true'}}}
    api_mock.obj = MagicMock(name="APIObjMock")
    d = DaemonSet(api_mock, scalable_mock)
    nodeselector = d.obj.get('spec')['nodeSelector']['non-existing']
    assert nodeselector == 'true'
    d.obj.get('spec').__delitem__('nodeSelector')
    assert scalable_mock['spec'].get('nodeSelector') is None


def test_daemonset_scale_down():
    api_mock = MagicMock(spec=NamespacedAPIObject, name="APIMock")
    scalable_mock = {'spec': {}}
    api_mock.obj = MagicMock(name="APIObjMock")
    d = DaemonSet(api_mock, scalable_mock)
    assert 'nodeSelector' not in d.obj['spec']
    d.obj.get('spec')['nodeSelector'] = {'non-existing': 'true'}
    assert scalable_mock['spec']['nodeSelector']['non-existing'] == 'true'


def test_stack():
    api_mock = MagicMock(spec=NamespacedAPIObject, name="APIMock")
    scalable_mock = {'spec': {'replicas': 3}}
    api_mock.obj = MagicMock(name="APIObjMock")
    d = Stack(api_mock, scalable_mock)
    r = d.replicas
    assert r == 3
    d.replicas = 10
    assert scalable_mock['spec']['replicas'] == 10
