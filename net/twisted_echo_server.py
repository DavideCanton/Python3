from twisted.internet import reactor, protocol


class EchoProtocol(protocol.Protocol):
    def dataReceived(self, data):
        self.transport.write(data)


class EchoFactory(protocol.ServerFactory):
    protocol = EchoProtocol


reactor.listenTCP(1234, EchoFactory())
reactor.run()
