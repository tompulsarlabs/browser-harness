"""Privacy regressions use synthetic data and intercept every analytics send."""
import json
from io import StringIO
from unittest.mock import patch

import pytest

from browser_harness import telemetry, run


@pytest.fixture(autouse=True)
def isolated(monkeypatch, tmp_path):
    monkeypatch.setattr(telemetry, '_config_dir', lambda: tmp_path)
    for name in telemetry.DISABLE_ENVS:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(telemetry, '_send_detached', lambda payload: None)


@pytest.mark.parametrize('config', [None, {}, {'disabled': False}, [], True, {'consent_version': True, 'disabled': False}])
def test_no_implicit_consent(config):
    if config is not None:
        telemetry._config_path().write_text(json.dumps(config))
    with patch.object(telemetry, '_send_detached') as send:
        telemetry.capture_cli_event(action='completed', command='script', task='SECRET')
        assert telemetry.status()['enabled'] is False
        assert telemetry.status()['install_id'] is None
        send.assert_not_called()


def test_consent_and_disable_override():
    assert telemetry.set_enabled(True)['enabled']
    with patch.dict('os.environ', {'BH_TELEMETRY': '0'}):
        assert not telemetry.is_enabled()
    assert not telemetry.set_enabled(False)['enabled']


def test_invalid_json_fails_closed():
    telemetry._config_path().write_text('{broken')
    assert not telemetry.is_enabled()


def test_secrets_never_leave_export_boundary(monkeypatch):
    telemetry.set_enabled(True)
    secret = 'SYNTHETIC_PRIVATE_CONTENT'
    for name in ['BH_CLIENT', 'BH_CLIENT_VERSION', 'BROWSER_USE_AGENT_MODEL', 'BROWSER_USE_MODEL_PROVIDER', 'BU_CDP_URL']:
        monkeypatch.setenv(name, secret)
    with patch.object(telemetry, '_send_detached') as send:
        telemetry.capture_cli_event(action='completed', command='script', task=secret,
            output=secret, output_length=24, error_message=secret, browser='local',
            steps=[{'helper':'fill_input', 'args':secret, 'error':secret, 'duration_seconds':0.2},
                   {'helper':secret, 'args':secret}], step_count=2, duration_seconds=1.5, exit_code=0)
        payload = send.call_args.args[0]
    assert secret not in json.dumps(payload)
    p = payload['properties']
    assert p['command'] == 'script' and p['step_count'] == 2
    assert p['duration_seconds'] == 1.5 and p['exit_code'] == 0
    assert p['steps'][0] == {'helper':'fill_input', 'duration_seconds':0.2, 'failed':True}
    assert p['steps'][1]['helper'] == 'other'
    assert p['$process_person_profile'] is False
    assert not {'task','output','error_message','cdp_url','client','model'} & p.keys()


def test_generic_capture_cannot_bypass_schema():
    telemetry.set_enabled(True)
    with patch.object(telemetry, '_send_detached') as send:
        telemetry.capture('SECRET_EVENT', {'value':'SECRET'})
        send.assert_not_called()
        telemetry.capture('cli_event', {'action':'SECRET','command':'SECRET','browser':'SECRET',
            'duration_seconds':float('nan'), 'exit_code':'SECRET', 'steps':[None, {'helper':'SECRET'}], 'value':'SECRET'})
        assert 'SECRET' not in json.dumps(send.call_args.args[0])
        assert send.call_args.args[0]['properties']['duration_seconds'] is None


def test_cli_preserves_result_without_capturing_output(monkeypatch):
    telemetry.set_enabled(True)
    monkeypatch.setattr(run, '_run', lambda args: print('SYNTHETIC_PAGE_RESULT'))
    monkeypatch.setattr(run, '_telemetry_browser', lambda task: 'local')
    with patch('sys.argv', ['browser-harness']), patch('sys.stdin', StringIO('SYNTHETIC_SCRIPT')), \
         patch('sys.stdout', new_callable=StringIO) as output, patch.object(telemetry, '_send_detached') as send:
        run.main()
        assert output.getvalue() == 'SYNTHETIC_PAGE_RESULT\n'
        assert 'SYNTHETIC' not in json.dumps(send.call_args.args[0])
        assert send.call_args.args[0]['properties']['output_length'] == len(output.getvalue())


def test_trace_does_not_retain_form_values():
    run._helper_trace.clear()
    def fail(value):
        raise ValueError(value)
    with pytest.raises(ValueError):
        run._traced('fill_input', fail)('SYNTHETIC_PASSWORD')
    assert 'SYNTHETIC_PASSWORD' not in json.dumps(run._helper_trace)
    assert run._helper_trace[-1]['failed'] is True
    run._helper_trace.clear()


@pytest.mark.parametrize('host', ['http://analytics.example', 'https://user:password@analytics.example', 'https://analytics.example/?secret=x'])
def test_unsafe_destination_never_spawns_sender(monkeypatch, host):
    monkeypatch.setenv('BH_POSTHOG_HOST', host)
    # Fixture replaces sender; retrieve the original function from its module source
    # through patch's saved reference below instead of running a network client.
    with patch.object(telemetry.subprocess, 'Popen') as spawn:
        ORIGINAL_SEND({})
        spawn.assert_not_called()


ORIGINAL_SEND = telemetry._send_detached


def test_https_sender_serializes_only_sanitized_metrics(monkeypatch):
    telemetry.set_enabled(True)
    monkeypatch.setattr(telemetry, '_send_detached', ORIGINAL_SEND)
    monkeypatch.setenv('BH_POSTHOG_HOST', 'https://analytics.example')
    with patch.object(telemetry.subprocess, 'Popen') as spawn:
        telemetry.capture_cli_event(action='error', command='script', task='SECRET_TASK',
            output='SECRET_PAGE', error_message='SECRET_ERROR', steps=[{'helper':'js', 'args':'SECRET_ARG'}])
        job = json.loads(spawn.return_value.stdin.write.call_args.args[0])
        assert job['url'] == 'https://analytics.example/i/v0/e/'
        assert 'SECRET' not in json.dumps(job)
        assert job['payload']['properties']['action'] == 'error'


def test_sender_refuses_redirects():
    import urllib.request
    job = {'url':'https://analytics.example/i/v0/e/', 'payload':{}, 'timeout':1}
    with patch('sys.stdin', StringIO(json.dumps(job))), patch.object(urllib.request, 'build_opener') as build:
        exec(telemetry._DETACHED_SENDER_SOURCE, {})
        handler = build.call_args.args[0]
        assert handler.redirect_request(None, None, 302, None, None, 'https://attacker.example') is None
        build.return_value.open.assert_called_once()
