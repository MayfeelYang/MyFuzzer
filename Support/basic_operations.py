__author__ = 'sf'
import sys

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from xml.dom import minidom
import urllib2

sys.path.append('../')
import config


class BasicOperations:
    def __init__(self):
        pass


class CloudOperations:
    def __init__(self):
        self.download_url = "http://%s/com-sm/download-file/" % config.RackeeperHOST
        self.upload_url = "http://%s/com-sm/upload-file/" % config.RackeeperHOST
        self.delete_url = "http://%s/com-sm/delete-file/" % config.RackeeperHOST
        self.reboot_url = "http://%s/com-cm/reboot-pu/" % config.RackeeperHOST

    def download_from_cloud(self, uri, path):
        """
        download a file from cloud and save to local path
        :param uri: index of file in cloud
        :param path: saved path that includes filename
        :return: "success" if download success, "fail" otherwise.
        """
        try:
            register_openers()
            datagen, headers = multipart_encode({"filename": uri, "storage_type": "ra"})
            request = urllib2.Request(self.download_url, datagen, headers)
            content = urllib2.urlopen(request).read()
            # download failed
            if r'<xml>' in content:
                print 'download file failed', content
                return 'fail'
            fh = open(path, "wb")
            fh.write(content)
            return "success"
        except Exception, e:
            print e
            return "fail"

    'upload result to swift'

    def upload_to_cloud(self, path):
        """
        upload a local file to cloud
        :param path: the path of local file
        :return: if upload success return uri, otherwise return fail
        """
        try:
            register_openers()
            datagen, headers = multipart_encode({"upload_file": open(path, "rb"), "storage_type": "ra"})
            request = urllib2.Request(self.upload_url, datagen, headers)
            result = urllib2.urlopen(request).read()
            dom = minidom.parseString(result)
            detail = dom.getElementsByTagName("detail")[0]
            item = detail.getElementsByTagName("item")[0]
            result_uri = item.getAttribute("file_uri")
            return result_uri
        except Exception, e:
            print e, 'upload error'
            return "fail"

    def del_from_cloud(self, uri):
        """
        delete one file in cloud
        :param uri: filename in cloud
        :return: 'success' if success,otherwise 'fail'
        """
        try:
            register_openers()
            datagen, headers = multipart_encode({"delete_file": uri, "storage_type": "ra"})
            request = urllib2.Request(self.delete_url, datagen, headers)
            result = urllib2.urlopen(request).read()
        except Exception, e:
            print 'exception happened when trying to delete file in cloud', e
            return 'fail'

        dom = minidom.parseString(result)
        result = dom.getElementsByTagName("result")[0]
        result = result.firstChild.nodeValue
        return result

    def reboot_cloud_pu(self, user_id, uuid):
        """
        Reboot a pu of cloud
        :param user_id: user id
        :param uuid: uuid of pu in cloud
        :return: return reboot result from cloud, return "fail" if reboot failed
        """
        try:
            register_openers()
            datagen, headers = multipart_encode({"user_id": str(user_id), "vm_uuid": str(uuid)})
            request = urllib2.Request(self.reboot_url, datagen, headers)
            result = urllib2.urlopen(request).read()
            dom = minidom.parseString(result)
            result = dom.getElementsByTagName("result")[0]
            result = result.firstChild.nodeValue
            return result
        except Exception, e:
            print e, 'upload error'
            return "fail"

    def transfer(self, host, local_path, remote_path):
        try:
            transport = paramiko.Transport((host, config.PORT))
            transport.connect(config.USERNAME, config.PASSWORD)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.put(local_path, remote_path)
        except Exception, e:
            print e


class FileOperations:
    def __init__(self):
        pass

    'copy file from source path to dest path'

    def copy(self, source_path, dest_path):

        cmd = "copy /y " + source_path + " " + dest_path + " >c:\\Inetpub\\ftproot\\copy.txt"
        try:
            os.system(cmd)
        except Exception, e:
            print e

    def copy_linux(self, source_path, dest_path):

        cmd = "cp  -r " + source_path + " " + dest_path
        try:
            os.system(cmd)
        except Exception, e:
            print e

    'copy files'

    def copy_dir_linux(self, source_path, dest_path):
        # for fil in source_path:
        cmd = "cp -r " + source_path + " " + dest_path + "/"
        try:
            os.system(cmd)
        except Exception, e:
            print e

    def make_file_path(self, path):
        try:
            print 'ok'
            if not os.path.exists(path):
                os.mkdir(path)
        except Exception, e:
            print e

    'ssh connect remote vm ,execute cmd'

    def ssh(self, vm_ip, cmd):
        print vm_ip, cmd
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(vm_ip, self.port, self.username, self.password)
            # openssh cmd should replace \\ by \\\\\\\\
            cmd = cmd.replace("\\", "\\\\\\\\")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print "result is :", stdout.read()
            self.global_stdout_channel.append(stdout.channel)
            time.sleep(2)
            ssh.close()
        except Exception, e:
            print e, 'ssh error'
            return "fail"

        'ssh under linux'

        def ssh_linux(self, vm_ip, cmd):
            print vm_ip, cmd
            try:
                print "ssh linux"
            except Exception, e:
                print e, "linux ssh error"

    'read or write from db'



    'zip file'

    def zip_dir_file(self, foldername, filename):
        zip = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(foldername):
            for filename in files:
                zip.write(join(root, filename).encode("gbk"))
            if len(files) == 0:
                zif = zipfile.ZipInfo((root + '/').encode("gbk" + "/"))
                zip.writestr(zif, "")
        zip.close()

    def delete_file(self, path):
        try:
            cmd = " rd  /S /Q " + path
            os.system(cmd)
            print "delete file dir ok"
        except Exception, e:
            print e, 'delete_file error'

    def unzip_file(self, source_file, dst_dir):
        # input_file = open(source_file, 'rb')
        zf = zipfile.ZipFile(source_file)
        for name in zf.namelist():
            zf.extract(name, dst_dir)
            # input_file.close()

    def zip_file(self, hash_path, dstfile):
        """zip files"""
        try:
            zip = zipfile.ZipFile(dstfile, 'w', zipfile.ZIP_DEFLATED)
            if os.path.isdir(hash_path):
                for dirpath, dirnames, filenames in os.walk(hash_path):
                    for filename in filenames:
                        zip.write(join(dirpath, filename), filename)

            elif os.path.isfile(hash_path):
                zip.write(hash_path, hash_path.split("\\")[-1])
            return "success"
        except Exception, e:
            print "zip file error:", e
            return "fail"

    '''def total_delete_linux(self,path):
        try:
            cmd="rm -f "+path
            #print cmd
            os.system(cmd)
        except Exception,e:
            print e,'delete error'''

    def delete_under_linux(self, path):
        try:
            cmd = "rm -rf " + path
            os.system(cmd)
            cmd = "mkdir " + path
            os.system(cmd)
        except Exception, e:
            print e, "delete err under linux"

    def delete_single_file(self, file_path):
        try:
            cmd = " del /f /s /q " + file_path + " >c:\\Inetpub\\ftproot\\delete_file.txt"
            # print cmd
            os.system(cmd)
            # print "delete file success"
        except Exception, e:
            print e, 'delete_file error'

    def execute_cmd(self, cmd):
        try:
            os.system(cmd)
        except Exception, e:
            time.sleep(random.randint(1, 5))
            print e, 'execute_cmd error'

    def gather_result(self, basic_op_obj, filename, result_id):
        'check if result directory exists'
        'add _ZIP_PATH check by zyy 2014-12-30'
        try:
            if not os.path.isdir(basic_op_obj._ZIP_PATH):
                os.mkdir(basic_op_obj._ZIP_PATH)
            if not os.path.isdir(basic_op_obj.ALL_RESULT_PATH):
                os.mkdir(basic_op_obj.ALL_RESULT_PATH)

            for vm_obj in self.executing_vm_list:
                result_uri = db_operations.get_vm_result_uri(basic_op_obj, vm_obj.vm.vm_id)
                if result_uri != 'null':
                    self.download(result_uri,
                                  basic_op_obj.ALL_RESULT_PATH + str(vm_id) + "_" + str(result_uri) + ".zip")
            zip_filename = filename + ".zip"
            dstfile = basic_op_obj._ZIP_PATH + zip_filename
            zip_result = self.zip_file(basic_op_obj.ALL_RESULT_PATH, dstfile)
            soft_result_uri = self.upload(dstfile)
            if soft_result_uri == "fail":
                print "upload failed"
            else:
                old_result_uri = db_operations.get_result_uri(basic_op_obj, result_id)
                if old_result_uri != 'null' and old_result_uri != soft_result_uri:
                    del_result = self.del_from_cloud(old_result_uri)
                    print "delete from cloud result: ", del_result
                db_operations.set_result_uri(basic_op_obj, soft_result_uri, result_id)
            self.delete_file(dstfile)
            cmd = " rd  /S /Q " + basic_op_obj._ZIP_PATH
            self.execute_cmd(cmd)
            cmd = "mkdir " + basic_op_obj._ZIP_PATH
            self.execute_cmd(cmd)
            return "success"
        except Exception, e:
            print "exception in gather result of basic_operation", e
            return e

    def check_whether_exit(self, filename, path):
        for root, dirs, files in os.walk(path):
            if filename in files:
                return root
            else:
                return 'NULL'

    def file_not_null(self, path):
        if len(os.listdir(path)):
            return True
        return False
