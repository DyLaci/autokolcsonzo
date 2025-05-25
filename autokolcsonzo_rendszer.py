from abc import ABC, abstractmethod
from datetime import date, timedelta

class Auto(ABC):

    def __init__(self, rendszam: str, tipus: str, berleti_dij_naponta: float):
        self._rendszam = rendszam
        self._tipus = tipus
        self._berleti_dij_naponta = berleti_dij_naponta

    @property
    def rendszam(self) -> str:
        return self._rendszam

    @property
    def tipus(self) -> str:
        return self._tipus

    @property
    def berleti_dij_naponta(self) -> float:
        return self._berleti_dij_naponta

    @abstractmethod
    def __str__(self) -> str:

        pass

class Szemelyauto(Auto):

    def __init__(self, rendszam: str, tipus: str, berleti_dij_naponta: float, ulesek_szama: int):
        super().__init__(rendszam, tipus, berleti_dij_naponta)
        self._ulesek_szama = ulesek_szama

    @property
    def ulesek_szama(self) -> int:
        return self._ulesek_szama

    def __str__(self) -> str:
        return (f"Személyautó - Rendszám: {self.rendszam}, Típus: {self.tipus}, "
                f"Bérleti díj/nap: {self.berleti_dij_naponta:.2f} Ft, Ülések száma: {self.ulesek_szama}")

class Teherauto(Auto):

    def __init__(self, rendszam: str, tipus: str, berleti_dij_naponta: float, max_terheles_kg: float):
        super().__init__(rendszam, tipus, berleti_dij_naponta)
        self._max_terheles_kg = max_terheles_kg

    @property
    def max_terheles_kg(self) -> float:
        return self._max_terheles_kg

    def __str__(self) -> str:
        return (f"Teherautó - Rendszám: {self.rendszam}, Típus: {self.tipus}, "
                f"Bérleti díj/nap: {self.berleti_dij_naponta:.2f} Ft, Max terhelés: {self.max_terheles_kg:.0f} kg")

class Berles:

    def __init__(self, auto: Auto, kezdo_datum: date):
        if not isinstance(auto, Auto):
            raise TypeError("Az 'auto' paraméternek 'Auto' típusúnak kell lennie.")
        if not isinstance(kezdo_datum, date):
            raise TypeError("A 'kezdo_datum' paraméternek 'date' típusúnak kell lennie.")
        self._auto = auto
        self._kezdo_datum = kezdo_datum
        self._veg_datum = kezdo_datum

    @property
    def auto(self) -> Auto:
        return self._auto

    @property
    def kezdo_datum(self) -> date:
        return self._kezdo_datum

    @property
    def veg_datum(self) -> date:
        return self._veg_datum

    def __str__(self) -> str:
        return (f"Bérlés: {self.auto.rendszam} ({self.auto.tipus}) - "
                f"Dátum: {self.kezdo_datum.strftime('%Y-%m-%d')} - "
                f"Bérleti díj: {self.auto.berleti_dij_naponta:.2f} Ft")

class Autokolcsonzo:

    def __init__(self, nev: str):
        self._nev = nev
        self._autok: list[Auto] = []
        self._berlesek: list[Berles] = []

    @property
    def nev(self) -> str:
        return self._nev

    def auto_hozzaadasa(self, auto: Auto):

        if not isinstance(auto, Auto):
            raise TypeError("Az 'auto' paraméternek 'Auto' típusúnak kell lennie.")
        self._autok.append(auto)

    def berles_foglalasa(self, rendszam: str, berles_datum: date) -> float | None:

        if berles_datum < date.today():
            print("Hiba: A bérlési dátum nem lehet korábbi az aktuális dátumnál.")
            return None

        auto_to_rent: Auto | None = None
        for auto in self._autok:
            if auto.rendszam == rendszam:
                auto_to_rent = auto
                break

        if not auto_to_rent:
            print(f"Hiba: Nincs ilyen rendszámú autó: {rendszam}")
            return None


        for berles in self._berlesek:
            if berles.auto.rendszam == rendszam and berles.kezdo_datum == berles_datum:
                print(f"Hiba: A {rendszam} rendszámú autó már foglalt {berles_datum} dátumon.")
                return None

        uj_berles = Berles(auto_to_rent, berles_datum)
        self._berlesek.append(uj_berles)
        print(f"Sikeresen bérelve a {rendszam} rendszámú autó {berles_datum} dátumra. Díj: {auto_to_rent.berleti_dij_naponta:.2f} Ft")
        return auto_to_rent.berleti_dij_naponta

    def berles_lemondasa(self, rendszam: str, berles_datum: date) -> bool:

        if berles_datum < date.today():
            print("Hiba: Korábbi bérlést nem lehet lemondani.")
            return False

        for berles in self._berlesek:
            if berles.auto.rendszam == rendszam and berles.kezdo_datum == berles_datum:
                self._berlesek.remove(berles)
                print(f"Sikeresen lemondva a {rendszam} rendszámú autó bérlése {berles_datum} dátumról.")
                return True
        print(f"Hiba: Nincs ilyen bérlés ({rendszam}, {berles_datum}) a rendszerben.")
        return False

    def berlesek_listazasa(self):

        if not self._berlesek:
            print("Nincsenek aktuális bérlések.")
            return

        print("\n--- Aktuális Bérlések ---")
        for berles in self._berlesek:
            print(berles)
        print("-------------------------\n")

    def autok_listazasa(self):

        if not self._autok:
            print("Jelenleg nincsenek autók a kínálatban.")
            return

        print("\n--- Kölcsönözhető Autók ---")
        for auto in self._autok:
            print(auto)
        print("--------------------------\n")



def adat_betoltes(kolcsonzo: Autokolcsonzo):

    # Autók
    kolcsonzo.auto_hozzaadasa(Szemelyauto("MLB-502", "Mazda 626 kombi", 8000.0, 5))
    kolcsonzo.auto_hozzaadasa(Szemelyauto("AOAD-456", "Suzuki Vitara", 17000.0, 4))
    kolcsonzo.auto_hozzaadasa(Teherauto("TGK-200", "Peugeot Partner", 35000.0, 1500))

    # Bérlések
    today = date.today()
    kolcsonzo.berles_foglalasa("MLB-502", today + timedelta(days=1)) # Holnapi bérlés
    kolcsonzo.berles_foglalasa("AOAD-456", today + timedelta(days=2)) # Holnaputáni bérlés
    kolcsonzo.berles_foglalasa("TgK-200", today + timedelta(days=3)) # Harmadik napi bérlés
    kolcsonzo.berles_foglalasa("MLB-502", today + timedelta(days=4)) # Negyedik napi bérlés (másik bérlés ugyanarra az autóra)


def main():

    kolcsonzo = Autokolcsonzo("Rentcar Autókölcsönző")
    adat_betoltes(kolcsonzo)

    print(f"Üdvözöljük a {kolcsonzo.nev} rendszerében!")

    while True:
        print("\nVálasszon a lehetőségek közül:")
        print("1. Autók listázása")
        print("2. Autó bérlése")
        print("3. Bérlés lemondása")
        print("4. Aktuális bérlések listázása")
        print("5. Kilépés")

        choice = input("Adja meg a választását (1-5): ")

        if choice == '1':
            kolcsonzo.autok_listazasa()
        elif choice == '2':
            rendszam = input("Adja meg a bérelni kívánt autó rendszámát: ").upper()
            datum_str = input("Adja meg a bérlés dátumát (YYYY-MM-DD formátumban): ")
            try:
                berles_datum = date.fromisoformat(datum_str)
                kolcsonzo.berles_foglalasa(rendszam, berles_datum)
            except ValueError:
                print("Érvénytelen dátum formátum. Kérjük, YYYY-MM-DD formátumot használjon.")
        elif choice == '3':
            rendszam = input("Adja meg a lemondani kívánt bérlés rendszámát: ").upper()
            datum_str = input("Adja meg a lemondandó bérlés dátumát (YYYY-MM-DD formátumban): ")
            try:
                berles_datum = date.fromisoformat(datum_str)
                kolcsonzo.berles_lemondasa(rendszam, berles_datum)
            except ValueError:
                print("Érvénytelen dátum formátum. Kérjük, YYYY-MM-DD formátumot használjon.")
        elif choice == '4':
            kolcsonzo.berlesek_listazasa()
        elif choice == '5':
            print("Viszlát!")
            break
        else:
            print("Érvénytelen választás. Kérjük, 1 és 5 közötti számot adjon meg.")

if __name__ == "__main__":
    main()