import phantom.rules as phantom
import json
from datetime import datetime, timedelta

def on_start(container):
    
    # call 'DW_VT' block
    DW_VT(container=container)

    return

def DW_VT(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):

    # collect data for 'DW_VT' call
    container_data = phantom.collect2(container=container, datapath=['artifact:*.cef.requestURL', 'artifact:*.id'])

    parameters = []
    
    # build parameters list for 'DW_VT' call
    for container_item in container_data:
        if container_item[0]:
            parameters.append({
                'url': container_item[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': container_item[1]},
            })

    phantom.act("url reputation", parameters=parameters, assets=['dw_vt'], callback=decision_1, name="DW_VT")    
    
    return

def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["DW_VT:action_result.summary.positives", ">", 0],
        ])

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        send_email_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return

def send_email_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'send_email_1' call

    parameters = []
    
    # build parameters list for 'send_email_1' call
    parameters.append({
        'body': "test",
        'to': "danajoyluck@gmail.com",
        'from': "",
        'attachments': "",
        'subject': "custom VT",
    })

    phantom.act("send email", parameters=parameters, assets=['smtp'], name="send_email_1")    
    
    return

def on_finish(container, summary):

    # This function is called after all actions are completed.
    # summary of all the action and/or all detals of actions 
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    return