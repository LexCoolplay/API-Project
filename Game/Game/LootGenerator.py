from WeaponDownloader import WeaponDownloader


class Treasure:
    def __init__(self):
        pass

    @staticmethod
    def get_pool(level):
        result = []
        weapon_loader = WeaponDownloader('weapons')
        weapons = weapon_loader.load()
        for weapon in weapons:
            if weapon.level == level:
                result.append(weapon)
        return result
