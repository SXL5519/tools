import jpype
import os
def getjvm():
    # jar_path = os.path.join(os.path.abspath('.'), r'/jar_package/mina-core-2.0.16.jar')
    jar_path = 'E:/tools/jar_package/mina-core-2.0.16.jar'
    dirs='E:/tools/jar_package'
    # jar包路径
    # jvmPath = jpype.getDefaultJVMPath()
    jvmPath = 'C:/Program Files/Java/jre1.8.0_144/bin/server/jvm.dll'
    jpype.startJVM(jvmPath,'-Djava.class.path=%s'%jar_path,'-Djava.ext.dirs=%s' %dirs)
    # jclass=jpype.JClass('org.apache.mina.transport.socket.nio.NioSocketConnector')
    # jclass = jpype.JPackage('org.apache.mina.transport.socket.nio').NioSocketConnector()
    # print(type(jclass))
    return jvmPath

def test_1():
    addr=jpype.JPackage('java.net').InetSocketAddress("192.168.1.23",9226)
    # addr=jclass_1()
    print(addr)
    return addr
def test(addr):
    # ip="192.168.1.23"
    # port=9226
    # a=(ip,port)
    jclass = jpype.JPackage('org.apache.mina.transport.socket.nio').NioSocketConnector()
    # jclass.setDefaultRemoteAddress(addr)
    cf = jclass.connect(addr)
    cf.awaitUninterruptibly()
    print(cf.getSession())

def shutdownJVM():
    jpype.shutdownJVM()


if __name__ == '__main__':
    jclass=getjvm()
    addr=test_1()
    test(addr)
    shutdownJVM()