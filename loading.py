import sys
import time

def ft_progress(lista: list):
    start_time = time.time()
    length_bar = 20
    prefix='Loading'
    lista_len = len(lista)
    for i, elem in enumerate(lista):
        percent = (i+1)/lista_len
        filled_length = int(length_bar * percent)
        bar = '█' * filled_length + '-' * (length_bar - filled_length)

        elapsed_time = time.time() - start_time
        # (total - (i+1))*elapsed / i+1 -> Regra de 3
        eta = round(((lista_len - (i+1)) * elapsed_time) / (i+1), 2)
        eta_str = time.strftime('%H:%M:%S', time.gmtime(eta))
        elapsed_time_str = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))

        sys.stdout.write(f"\rETA: {eta_str} [{percent:.1%}] {prefix} |{bar}| {i+1}/{lista_len} elapsed time: {elapsed_time_str}")
        sys.stdout.flush()
        yield elem

def main():
    a_list = range(1000)
    ret = 0
    for elem in ft_progress(a_list):
        ret += (elem + 3) % 5
        time.sleep(0.02)
    print()
    print(ret)

main()