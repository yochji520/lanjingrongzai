#-*- coding: utf-8 -*-


class CheckMysql():
    def __init__(self,host):
        self.host = host
        try:
            self.conn = MySQLdb.connect(host=self.host, port=3306, user='root', passwd='123456',
                              db='',charset="utf8")
        except Exception as err:
            print "MySQL Connection failed!!! %s" % err
        self.cur = self.conn.cursor()

    def conn_query(self,ro_sql):
        self.cur.execute(ro_sql)
        result = self.cur.fetchall()
        return result

    def close_conn(self):
        self.cur.close()
        self.conn.close()

    def check_slave_behind(self):
        ro_sql = "show slave status;"
        ret = self.conn_query(ro_sql)
        self.close_conn()
        return ret

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
    try:
        respon = requests.post(apiurl, data=json.dumps(pars))
    except Exception as err:
        print "sdk request is failed!!!"
    return  respon.json()['data']['info']


if __name__ == "__main__":
    for mapinfo in pull_rongzai_info():
        conn =  CheckMysql(mapinfo['binstance_ip'])
        ret = conn.check_slave_behind()
        io_thread = ret[0][10]
        sql_thread = ret[0][11]
        slag = ret[0][32]
        if slag == 0 and io_thread == sql_thread:
            print  "ip:%s,延迟时间:%s,IO线程状态:%s,SQL线程状态:%s" % (
                mapinfo['binstance_ip'], slag, str(io_thread), str(sql_thread))




