from pathlib import Path


class Utils:
    def __init__(self, cwd: Path) -> None:
        with open(cwd / Path('sen_v2.txt'), 'r', encoding='utf-8') as f:
            self.data = f.readlines()

    def get_data(self) -> list:
        return self.data

    def get_beyts_by_mesras(self, mesras: list) -> list:
        beyts = []
        for mesra in mesras:
            idx = self.data.index(mesra)
            if idx % 2 == 0:
                beyt = mesra + "####" + self.data[idx + 1]
            else:
                beyt = self.data[idx - 1] + "####" + mesra
            beyts.append(beyt.strip().replace('\n', ''))
        return beyts
