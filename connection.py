import nfc
import time

class Connection:
    def __init__(self):
        self.SYSTEM_CODE = 0xfe00
        self.data = {'id': '', 'name': '', 'balance': ''}

    def check_connect(self):
        with nfc.ContactlessFrontend('usb') as clf:
            target_res = clf.sense(nfc.clf.RemoteTarget("212F"), iterations=5 , interval=0.5)
            if not target_res is None:
                tag = nfc.tag.activate(clf, target_res)
                self.on_connect(tag)

    def on_connect(self, tag):
        if tag.type == "Type3Tag":
            system_codes = tag.request_system_code()
            if self.SYSTEM_CODE in system_codes:
                return self.check_system(tag, self.SYSTEM_CODE)

    def check_system(self, tag, system_code):
        idm, pmm = tag.polling(self.SYSTEM_CODE)
        tag.idm, tag.pmm, tag.sys = idm, pmm, self.SYSTEM_CODE
        self.data = {"id": self.get_student_id(tag),
                    "name": self.get_student_name(tag),
                    "balance": self.get_balance(tag),
                    }

    def get_data(self):
        return self.data

    def get_student_id(self, tag):
        STUDENT_SERVICE_CODE = 0x1a8b
        sc = nfc.tag.tt3.ServiceCode(STUDENT_SERVICE_CODE >> 6, STUDENT_SERVICE_CODE & 0x3f)
        bc = nfc.tag.tt3.BlockCode(0, service=0) # student id
        data = tag.read_without_encryption([sc], [bc])
        return data[2:8].decode("utf-8")

    def get_student_name(self, tag):
        STUDENT_SERVICE_CODE = 0x1a8b
        sc = nfc.tag.tt3.ServiceCode(STUDENT_SERVICE_CODE >> 6, STUDENT_SERVICE_CODE & 0x3f)
        bc = nfc.tag.tt3.BlockCode(1, service=0) # name
        data = tag.read_without_encryption([sc], [bc])
        return data[0:16].decode("shift_jis").strip('\u0000')

    def get_balance(self, tag):
        BALANCE_SERVICE_CODE = 0x50d7
        sc = nfc.tag.tt3.ServiceCode(BALANCE_SERVICE_CODE >> 6, BALANCE_SERVICE_CODE & 0x3f)
        bc = nfc.tag.tt3.BlockCode(0, service=0) # balance
        data = tag.read_without_encryption([sc], [bc])
        return int.from_bytes(data[0:5], byteorder='little', signed=True)
