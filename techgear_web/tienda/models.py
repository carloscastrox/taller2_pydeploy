class Producto:
    def __init__(self, id, nombre, descripcion, precio, stock):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            nombre=data.get("nombre"),
            descripcion=data.get("descripcion"),
            precio=data.get("precio"),
            stock=data.get("stock")
        )