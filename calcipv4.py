import re


class CalcIPv4:
    def __init__(self, ip, mascara=None, prefixo=None):
        self.ip = ip
        self.mascara = mascara
        self.prefixo = prefixo
        self._definir_broadcast_()
        self._definir_rede_()

    @property
    def rede(self):
        return self._rede

    @property
    def broadcast(self):
        return self._broadcast

    @property
    def numero_ips(self):
        return self._pegar_numero_ips_()

    @property
    def ip(self):
        return self._ip

    @property
    def mascara(self):
        return self._mascara

    @property
    def prefixo(self):
        return self._prefixo

    @ip.setter
    def ip(self, valor):
        if not self._valida_ip_(valor):
            raise ValueError('IP inválido.')

        self._ip = valor
        self._ip_binario = self._ip_para_binario_(valor)

    @mascara.setter
    def mascara(self, valor):
        if not valor:
            return

        elif not self._valida_ip_(valor):
            raise ValueError('Máscara inválida.')

        self._mascara = valor
        self._mascara_binario = self._ip_para_binario_(valor)

        if not hasattr(self, 'prefixo'):
            self.prefixo = self._mascara_binario.count('1')

    @prefixo.setter
    def prefixo(self, valor):
        if not valor:
            return
        elif not isinstance(valor, int):
            raise TypeError('Prefixo precisa ser inteiro.')
        elif valor > 32:
            raise TypeError('Prefixo precisa ter 32bits.')
        self._prefixo = valor
        self._mascara_binario = str(valor * '1').ljust(32, '0')

        if not hasattr(self, 'mascara'):
            self.mascara = self._binario_para_ip_(self._mascara_binario)

    @staticmethod
    def _valida_ip_(ip):
        regexp = re.compile(r'^([0-9]{1,3}).([0-9]{1,3}).([0-9]{1,3}).([0-9]{1,3})$')
        if regexp.search(ip):
            return True

    @staticmethod
    def _ip_para_binario_(ip):
        blocos = ip.split('.')
        blocos_binarios = [bin(int(x))[2:].zfill(8) for x in blocos]
        return ''.join(blocos_binarios)

    @staticmethod
    def _binario_para_ip_(binario):
        n = 8
        blocos = [str(int(binario[i:n+i], 2)) for i in range(0, 32, 8)]
        return '.'.join(blocos)

    def _definir_broadcast_(self):
        host_bits = 32 - self.prefixo
        self._broadcast_binario = self._ip_binario[:self.prefixo] + (host_bits * '1')
        self._broadcast = self._binario_para_ip_(self._broadcast_binario)
        return self._broadcast

    def _definir_rede_(self):
        host_bits = 32 - self.prefixo
        self._rede_bin = self._ip_binario[:self.prefixo] + (host_bits * '0')
        self._rede = self._binario_para_ip_(self._rede_bin)
        return self._broadcast

    def _pegar_numero_ips_(self):
        return 2 ** (32 - self.prefixo)
