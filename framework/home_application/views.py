# -*- coding: utf-8 -*-

from common.mymako import render_mako_context
from blueking.component.shortcuts import get_client_by_request
from home_application.common2 import get_business_by_user
from common.mymako import render_mako_context, render_json
from conf.default import APP_TOKEN, APP_ID, BK_PAAS_HOST
import httplib2
import json
from common.log import logger
from home_application.common2 import execute_job


def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/home.html')


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')


def host_status(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/host.html')


def get_biz_list(request):
    username = request.user.username
    https = httplib2.Http()
    kwargs = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": username,
    }
    url = '%s/api/c/compapi/v2/cc/search_business/' % (BK_PAAS_HOST)
    header = {'Content-Type': 'application/json'}
    response, content = https.request(url, 'POST', headers=header, body=json.dumps(kwargs))
    content = json.loads(content)
    if response.status == 200:
        return_data = []
        for i in content['data']['info']:
            return_data.append({'biz_id': i['bk_biz_id'], 'biz_name': i['bk_biz_name']})
    else:
        logger.error('获取业务失败')
        return render_json({'result': False, 'data': []})
    return render_json({'result': True, 'data': return_data})


def get_cluster(request):
    username = request.user.username
    biz_id = request.POST['biz_id']
    https = httplib2.Http()
    kwargs = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": username,
        "bk_biz_id": biz_id
    }
    url = '%s/api/c/compapi/v2/cc/search_set/' % (BK_PAAS_HOST)
    header = {'Content-Type': 'application/json'}
    response, content = https.request(url, 'POST', headers=header, body=json.dumps(kwargs))
    content = json.loads(content)
    if response.status == 200:
        return_data = []
        for i in content['data']['info']:
            return_data.append({'bk_set_id': i['bk_set_id'], 'bk_set_name': i['bk_set_name']})
    else:
        logger.error('获取集群失败')
        return render_json({'result': False, 'data': []})
    return render_json({'result': True, 'data': return_data})


def search_host_info(request):
    username = request.user.username
    biz_id = request.POST['biz_id']
    set_id = int(request.POST['set_id'])
    https = httplib2.Http()
    kwargs = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": username,
        "bk_biz_id": biz_id,
        "condition": [
            {
                "bk_obj_id": "set",
                "fields": [],
                "condition": [
                    {
                        "field": "bk_set_id",
                        "operator": "$eq",
                        "value": set_id
                    }
                ]
            }]
    }
    url = '%s/api/c/compapi/v2/cc/search_host/' % (BK_PAAS_HOST)
    header = {'Content-Type': 'application/json'}
    response, content = https.request(url, 'POST', headers=header, body=json.dumps(kwargs))
    content = json.loads(content)
    if response.status == 200:
        return_data = []
        for i in content['data']['info']:
            return_data.append({'bk_host_innerip': i['host']['bk_host_innerip'], 'bk_os_name': i['host']['bk_os_name'],
                                'bk_host_name': i['host']['bk_host_name'],
                                'bk_inst_name': i['host']['bk_cloud_id'][0]['bk_inst_name'],
                                'bk_inst_id': i['host']['bk_cloud_id'][0]['bk_inst_id']})
    else:
        logger.error('获取主机信息失败')
        return render_json({'result': False, 'data': []})
    return render_json({'result': True, 'data': return_data})


def execute_task(request):
    execute_job(request)

