import csv

class Truck:
    def __init__(self):
        self.file = "olaylar.csv"
        self.truckDict = {} # Tır Sözlüğü
        self.truckPlateList = [] # Tır Plaka Listesi
        self.truckLoadList = [] # Tır Yük Listesi
        self.truckTimeList = [] # Tır Zaman Listesi
        self.truckCountryList = [] # Tır Ülke Listesi
        self.createTruckDict()         
        self.createTruckPlateList()
        self.createTruckLoadList()   # Liste Oluşturmalar.
        self.createTruckTimeList()
        self.createTruckCountryList()

    def createTruckDict(self):      # Csv dosyasını sözlüğe çevirme.
        with open(self.file, "r") as file:
            truck = csv.DictReader(file)
            self.truckDict = sorted(truck, key=lambda x: x['geliş_zamanı'])

    def createTruckLoadList(self):  # Tır yüklerini listeye atma.
        for i in self.truckDict:
            self.truckLoadList.append(int(i["yük_miktarı"]))

    def createTruckCountryList(self): # Tır ülkelerini listeye atma.
        for i in self.truckDict:
            self.truckCountryList.append(i["ülke"])

    def createTruckPlateList(self): # Tır plakalarını listeye atma.
        for i in self.truckDict:
            plate = i["tır_plakası"]
            plateNumber = plate[-3:]
            self.truckPlateList.append(plateNumber)
    
    def createTruckTimeList(self):  # Tır zamanlarını listeye atma.
        for i in self.truckDict:
            self.truckTimeList.append(int(i["geliş_zamanı"]))
        self.truckTimeList.sort()

class Ship:
    def __init__(self):
        self.file = "gemiler.csv"
        self.sortedDict = {} # Gemi Sözlüğü
        self.shipNameList = [] # Gemi Adları Listesi
        self.shipCapacityList = [] # Gemi Kapasite Listesi
        self.shipLoadList = [] # Geminin %95'lik Kapasite Listesi
        self.createShipNameList() # Listeleri oluşturma.
        self.createShipDict()
        self.createShipCapacityList()
        self.shipCondition()

    def createShipDict(self):     # Csv dosyasını sözlüğe çevirme.
        with open(self.file, "r") as file:
            shipDict = csv.DictReader(file)
            self.sortedDict = sorted(shipDict, key=lambda x: x['gemi_adı'])

    def createShipCapacityList(self):   # Gemi kapasitelerini listeye atma.
        for i in self.sortedDict:
            self.shipCapacityList.append(int(i["kapasite"]))
         
    def createShipNameList(self):       # Gemi isimlerini listeye atma.
        for i in range(1,451):
            self.shipNameList.append(str(i))
        
        for index, value in enumerate(self.shipNameList):
            if len(value) == 1:
                self.shipNameList[index] = f"00{value}"
            elif len(value) == 2:
                self.shipNameList[index] = f"0{value}"

    def getShipLoad(self, name):    # Gemi adı ile geminin %95lik kapasitesini alma.
        for i in self.sortedDict:
            if name == i["gemi_adı"]:
                return int(int(i["kapasite"]) * 95 / 100)

    def getShipCapacity(self, name):    # Gemi adı ile kapasitesini alma.
        for i in self.sortedDict:
            if name == i["gemi_adı"]:
                return int(i["kapasite"])
    
    def getShipTime(self, name):    # Gemi adı ile zamanını alma.
        for i in self.sortedDict:
            if name == i["gemi_adı"]:
                return int(i["geliş_zamanı"])

    def getShipCountry(self, name): # Gemi adı ile ülkesini alma.
        for i in self.sortedDict:
            if name == i["gemi_adı"]:
                return i["gidecek_ülke"]
    
    def shipCondition(self):    # Gemi %95lik kapasites listesi.
        for i in self.shipCapacityList:
            self.shipLoadList.append(int(i) * 95 / 100)
        return self.shipLoadList

class Stack:
	def __init__(self):
		self._theItems = list() # Yığını liste kullanarak yapıyoruz.

	def isEmpty(self):  # Yığının boş olup olmadığını kontrol etme.
		return len(self) == 0

	def __len__(self):  # Yığının uzunluğu
		return len(self._theItems)

	def peek(self): # En üstteki değere bakma.
		assert not self.isEmpty(), "Can't peek at an empty stack."
		return self._theItems[-1]

	def pop(self):  # Üstteki değeri çıkartma.
		assert not self.isEmpty(), "Can't pop at an empty stack."
		return self._theItems.pop()

	def push(self, item): # Değeri yığına ekleme.
		self._theItems.append(item)

	def __str__(self):  # Çıktı vermesi için str metodu.
		return str(self._theItems)
     
class Harbor:    # Liman sınıfı.
    def __init__(self):
        self.ship = Ship()  # Gemi objesi
        self.truck = Truck()    # Tır objesi
        self.istifAlani = Stack()   # İstif Alanı 1
        self.istifAlani2 = Stack()  # İstif Alanı 2

    def indir_yukle(self): # İndirme ve yükleme fonksiyonu 
        for indexShip, ship in enumerate(self.ship.shipNameList): 
            gemiYük = 0 # Anlık gemi yükü.
            for indexTruck, truck in enumerate(self.truck.truckPlateList):
                if self.ship.getShipTime(ship) < self.truck.truckTimeList[indexTruck]: # Gemi ve tır zamanları karşılaştırma.
                    if self.ship.getShipCountry(ship) == self.truck.truckCountryList[indexTruck]: # Gemi ve tır ülkesi karşılaştırma.
                        gemiYük += self.truck.truckLoadList[indexTruck] # Yükü gemiye yükleme.
                        if gemiYük > self.ship.shipLoadList[indexShip] - 10: # Gemi yük kontrolü.
                            print(f"{self.ship.getShipTime(ship)} zamanında gelen {ship} gemisi {gemiYük} yükü ile {self.ship.getShipCountry(ship)} ülkesine yola çıkmıştır.")
                            break
                    else:
                        if len(self.istifAlani) < 22: # İstif alanı kontrolü.
                            self.istifAlani.push((truck, self.truck.truckCountryList[indexTruck], self.truck.truckLoadList[indexTruck])) # Gelen yükleri istif alanına boşaltma.
                        else:
                            while not self.istifAlani.isEmpty() and self.istifAlani.peek()[1] != self.ship.getShipCountry(ship):
                                self.istifAlani2.push(self.istifAlani.pop()) # Yüklenecek yükün bulunması için üstteki yüklerin 2. istif alanına taşınması.
                                if not self.istifAlani.isEmpty() and self.istifAlani.peek()[1] == self.ship.getShipCountry(ship):
                                    gemiYük += self.istifAlani.pop()[2]

h = Harbor()
h.indir_yukle()
                            