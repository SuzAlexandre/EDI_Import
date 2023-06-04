from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, NVARCHAR, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime


Base = declarative_base()


class Part(Base):
    __tablename__ = "parts"

    serial_number = Column("serial_number", NVARCHAR(128), primary_key=True)
    so_number = Column("so_number", Integer, ForeignKey("so_numbers.so_number"))
    create_time = Column("create_time", DateTime, default=datetime.datetime.now())
    ht_batch_number = Column("ht_batch_number", NVARCHAR(10))

    def __init__(self, serial_number, so_number):
        self.serial_number = serial_number
        self.so_number = so_number
        self.create_time = datetime.datetime.now()


    def __repr__(self):
        return f"serial number: {self.serial_number} is a part type {self.so_number} made on " \
               f"{self.create_time.date()} at {self.create_time.time()}"


class SONumber(Base):
    __tablename__ = "so_numbers"

    so_number = Column("so_number", Integer, primary_key=True)
    revision = Column("revision", Integer)
    platform = Column("platform", NVARCHAR(50))
    hand = Column("hand", NVARCHAR(10))
    description = Column("description", NVARCHAR(50))

    def __init__(self, so_number, platform, hand):
        self.so_number = so_number
        self.platform = platform
        self.hand = hand
        self.description = f"{platform} - {hand}"
        self.revision = 0

    def update_revision_number(self, revision):
        self.revision = revision if revision > self.revision else self.revision


class EdiDemands(Base):
    __tablename__ = "edi_demands"

    demand_id = Column("id", Integer, primary_key=True)
    so_number = Column("so_number", Integer, ForeignKey("so_numbers.so_number"))
    quantity = Column("quantity", Integer)


class ProcessStep(Base):
    __tablename__ = "process_steps"

    process_id = Column("process_id", Integer, primary_key=True)
    process_description = Column("process_description", NVARCHAR(128))

    def __init__(self, process_description):
        self.process_description = process_description


class Equipment(Base):
    __tablename__ = "equipments"

    equipment_id = Column("equipment_id", Integer, primary_key=True)
    equipment_type = Column("equipment_type", Integer)
    equipment_name = Column("equipment_name", NVARCHAR(50))

    def __init__(self, equipment_type, equipment_name):
        self.equipment_name = equipment_name
        self.equipment_type = equipment_type


class ProcessProfileAssignment(Base):
    __tablename__ = "process_profile_assignment"

    item_no = Column("item_no", Integer, primary_key=True)
    process_id = Column("process_id", Integer, ForeignKey("process_steps.process_id"))
    process_step_number = Column("process_step_number", Integer)
    equipment_id = Column("equipment_id", Integer, ForeignKey("equipments.equipment_id"))
    so_number = Column("so_number", Integer, ForeignKey("so_numbers.so_number"))

    def __init__(self, process_id, process_step_number, equipment_id, so_number):
        self.process_id = process_id
        self.process_step_number = process_step_number
        self.equipment_id = equipment_id
        self.so_number = so_number


# Connect to database
engine = create_engine("sqlite:///mydb.db", echo=True)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
