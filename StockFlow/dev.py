from app.objects.models.Cargo import Cargo

if __name__ == "__main__":
    car = Cargo(1, 'Lenhador', '00.000.000/0001-00')
    print(car.create().msg)
