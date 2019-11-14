#-*- coding: utf-8 -*-
#
#设置主节点为只读
#

"""
通过获取蓝鲸容灾信息，设置主节点为只读
"""
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.abstract_model import AbstractModel
from tencentcloud.cdb.v20170320.cdb_client import CdbClient
import json


"""
# CDB支持灾备回切python SDK 扩展。
# 官网SDK没有提供的接口，都可以通过类似的写法来扩展SDK，支持其它官网未公开的API。
"""

class ModifyDBInstanceReadOnlyStatusRequest(AbstractModel):
    """修改MySQL云数据库实例状态为只读请求
    """

    def __init__(self):
        """
        :param InstanceId: 实例ID，格式如：cdb-c1nl9rpv，与云数据库控制台页面中显示的实例ID相同，可使用[查询实例列表](https://cloud.tencent.com/document/api/236/15872) 接口获取，其值为输出参数中字段 InstanceId 的值。
        :type InstanceId: str
        """
        self.InstanceId = None
        self.ReadOnly = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.ReadOnly = params.get("ReadOnly")


class ModifyDBInstanceReadOnlyStatusResponse(AbstractModel):
    """修改MySQL云数据库实例状态为只读响应
    """

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class SwitchDrMasterSrcInfo(AbstractModel):
    def __init__(self):
        self.InstanceId = None
        self.IsOverrideRoot = None
        self.RegionId = None
        self.ZoneId = None

    def _deserialize(self,params):
        self.InstanceId = params.get("InstanceId")
        self.IsOverrideRoot = params.get("IsOverrideRoot")
        self.RegionId = params.get("RegionId")
        self.ZoneId = params.get("ZoneId")


class SwitchDrMasterDstInfo(AbstractModel):
    def __init__(self):
        self.InstanceId = None
        self.RegionId = None
        self.ZoneId = None

    def _deserialize(self,params):
        self.InstanceId = params.get("InstanceId")
        self.RegionId = params.get("RegionId")
        self.ZoneId = params.get("ZoneId")


class SwitchDrMasterRoleRequest(AbstractModel):
    """
    """
    def __init__(self):
        self.SrcInfo = None
        self.DstInfo = None

    def _deserialize(self,params):
        if params.get("SrInfo") is not None:
            self.SrcInfo = SwitchDrMasterSrcInfo()
            self.SrcInfo._deserialize(params.get("SrcInfo"))
        if params.get("DstInfo") is not None:
            self.DstInfo = SwitchDrMasterDstInfo()
            self.DstInfo._deserialize(params.get("DstInfo"))


class SwitchDrMasterRoleResponse(AbstractModel):
    """
    """

    def __init__(self):
        """
        """
        self.RequestId = None
        self.AsyncRequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")
        self.AsyncRequestId = params.get("AsyncRequestId")


class SwitchDrInstanceToMasterRequest(AbstractModel):
    def __init__(self):
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class SwitchDrInstanceToMasterResponse(AbstractModel):
    def __init__(self):
        """
        """
        self.RequestId = None
        self.AsyncRequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")
        self.AsyncRequestId = params.get("AsyncRequestId")


class CdbDrMasterSwitchClient(CdbClient):
    def __do_request(self, actionName, request, responseModel):
        try:
            params = request._serialize()
            body = self.call(actionName, params)
            response = json.loads(body)
            #print response
            if "Error" not in response["Response"]:
                responseModel._deserialize(response["Response"])
                return responseModel
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise e
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def ModifyDBInstanceReadOnlyStatus(self, request):
        actionName = "ModifyDBInstanceReadOnlyStatus"
        response = ModifyDBInstanceReadOnlyStatusResponse()
        #res = self.__do_request(actionName, request, response)
        #print res["RequestId"]
        return self.__do_request(actionName, request, response)

    def SwitchDrMasterRole(self, request):
        actionName = "SwitchDrMasterRole"
        response = SwitchDrMasterRoleResponse()
        return self.__do_request(actionName, request, response)

    def SwitchDrInstanceToMaster(self, request):
        actionName = "SwitchDrInstanceToMaster"
        response = SwitchDrInstanceToMasterResponse()
        return self.__do_request(actionName, request, response)


#拉取容灾信息
def pull_rongzai_info():
    """
        获取容灾实例印象列表
    :return:  respon.json()['data']['info']  返回所有容灾映射列表
    """
    import json
    import requests
    apiurl = "http://fatbkpaas.uu.cc/api/c/compapi/v2/cc/search_inst/"
    pars = {
        "bk_app_code": "idrdbm",
        "bk_app_secret": "d573be17-85a7-4341-a078-311c046e212b",
        "bk_username": "jack.you",
        "bk_obj_id": "ba_mb_map",
        "bk_supplier_account": "0",
        "page": {
            "start": 0,
            "limit": 10,
            "sort": "instance_id"
        }
    }

    respon = requests.post(apiurl, data=json.dumps(pars))
    return  respon.json()['data']['info']


#设置为只读
def set_readonly(project_name,minstance_ip):
    """
    设置成功和失败
    :return: string ,返回success和failed
    """
    cred = credential.Credential('xxxx','xxxx')
    Region = 'gz-guangzhou'
    client = CdbDrMasterSwitchClient(cred, Region)
    setReadOnlyRequest = ModifyDBInstanceReadOnlyStatusRequest()
    setReadOnlyRequest.InstanceId = str(minstance_ip.strip('\r\n'))
    setReadOnlyRequest.ReadOnly = 1
    setReadOnlyResponse = client.ModifyDBInstanceReadOnlyStatus(setReadOnlyRequest)
    print '%s 开启只读成功，任务ID:%s' % (minstance_ip.strip('\r\n'), setReadOnlyResponse)


if __name__ == '__main__':
    resv =pull_rongzai_info()
    for  r in resv:
        project_name = r['project_name']
        minstance_ip = r['minstance_ip']
        set_readonly(project_name,minstance_ip)

