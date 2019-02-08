from multiprocessing import Process

import pituophis


def reg():
    pituophis.serve("127.0.0.1", 50400, pub_dir='pub/', tls=False)  # typical Gopher port is 70


def tls():
    pituophis.serve("127.0.0.1", 50500, pub_dir='pub/', tls=True,
                    tls_cert_chain='cacert.pem', tls_private_key='privkey.pem')  # typical S/Gopher port is 105


if __name__ == '__main__':
    processes = [Process(target=reg),
                 Process(target=tls)]
    for process in processes:
        process.start()
