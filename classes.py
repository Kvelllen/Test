import datetime
import abc


class Lists(abc.ABC):
    globalID = 0
    orderSet = set()
    customerSet = set()

    @abc.abstractmethod
    def add_to_set(self, object):
        pass


class Order(Lists):
    minAmount = 100
    types = ['A', 'B', 'C']
    specialFunctionsList = [
        "Get orders",
        "-- Customers list",
        "-- Most popular type",
        "-- Average amount",
        "-- Most expensive order",
        "-- Customer who paid the most"
    ]

    def __init__(self, id, type, amount, price, manager, customer, dateCreation, dateCompletion):
        self.id = id
        self.type = type
        self.amount = amount
        self.price = price
        self.manager = manager
        self.customer = customer
        self.dateCreation = dateCreation or self.setDateCreation()
        self.dateCompletion = dateCompletion

    @classmethod
    def setDateCreation(cls):
        x0 = str(datetime.datetime.now()).replace('/', '')
        x1 = x0[:x0.rfind('.')]
        return x1

    @classmethod
    def add_to_set(cls, object):
        Order.orderSet.add(object)


class Customer(Lists):
    def __init__(self, name, adress, telephone):
        self.name = name
        self.adress = adress
        self.telephone = telephone

    @classmethod
    def add_to_set(cls, object):
        Customer.customerSet.add(object)


class Manager:
    def __init__(self, name, adress, telephone):
        self.name = name
        self.adress = adress
        self.telephone = telephone
