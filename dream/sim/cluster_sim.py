"""
Bloomrise - kume bulunurlugu olcumu.

Soru: Rastgele bir tahtaya ilk bakildiginda, N veya daha buyuk
      ayni renkli bitisik bir grup gorme ihtimali nedir?

Yontem: Olasilik formulu YOK. 4.000 tahta uret, say, orani al.
        (Monte Carlo simulasyonu)
"""
import random

R = C = 8          # tahta 8x8
TRIALS = 4000      # kac tahta uretilecek


def largest_groups(colours):
    """Bir tahta uret, icindeki butun bitisik ayni-renk gruplarinin boyutlarini dondur."""
    board = [[random.randrange(colours) for _ in range(C)] for _ in range(R)]
    seen = [[False] * C for _ in range(R)]
    sizes = []

    for y in range(R):
        for x in range(C):
            if seen[y][x]:
                continue
            # flood fill: bu karodan basla, ayni renkteki komsulara yuru
            colour = board[y][x]
            stack, group = [(y, x)], 0
            seen[y][x] = True
            while stack:
                cy, cx = stack.pop()
                group += 1
                for ny, nx in ((cy-1, cx), (cy+1, cx), (cy, cx-1), (cy, cx+1)):
                    if 0 <= ny < R and 0 <= nx < C and not seen[ny][nx] \
                            and board[ny][nx] == colour:
                        seen[ny][nx] = True
                        stack.append((ny, nx))
            sizes.append(group)
    return sizes


def run(colours):
    thresholds = [3, 5, 7, 9]
    boards_with = {t: 0 for t in thresholds}   # en az bir tane iceren tahta sayisi
    total_count = {t: 0 for t in thresholds}   # toplam grup sayisi

    for _ in range(TRIALS):
        sizes = largest_groups(colours)
        for t in thresholds:
            n = sum(1 for s in sizes if s >= t)
            total_count[t] += n
            if n:
                boards_with[t] += 1

    print("\n%d renk, %d tahta, %dx%d" % (colours, TRIALS, R, C))
    print("%-8s %-22s %s" % ("Kume", "Tahta basina ortalama", "En az bir tane iceren tahta"))
    for t in thresholds:
        print("%-8s %-22.2f %.0f%%" % (
            "%d+" % t,
            total_count[t] / TRIALS,
            100.0 * boards_with[t] / TRIALS))


if __name__ == "__main__":
    random.seed(1)
    run(4)
    run(5)
