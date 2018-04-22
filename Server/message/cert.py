from .base import BaseMessage


class CertificateSigningRequestMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)

    def _init_type(self):
        self.type = 'CertificateSigningRequestMessage'

    def _parse_dict(self, data):
        super()._parse_dict(data)
        self.csr = data['csr']

    def to_dict(self):
        data = super().to_dict()
        data['csr'] = self.csr
        return data


class CertificateRequestMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)

    def _init_type(self):
        self.type = 'CertificateRequestMessage'

    def _parse_dict(self, data):
        super()._parse_dict(data)
        self.request_user = data['request_user']

    def to_dict(self):
        data = super().to_dict()
        data['request_user'] = self.request_user
        return data

class CertificateInstallMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)

    def _init_type(self):
        self.type = 'CertificateInstallMessage'

    def _parse_dict(self, data):
        super()._parse_dict(data)
        self.cert_user = data.get('cert_user')
        self.cert = data.get('cert')

    def to_dict(self):
        data = super().to_dict()
        data['cert_user'] = self.cert_user
        data['cert'] = self.cert
        return data



