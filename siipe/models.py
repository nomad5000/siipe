from django.db import models

# Create your models here.

from django.db import models
from model_utils.models import TimeStampedModel

# Tiquete de Bascula
class WeightTicketModel(TimeStampedModel):
    # 🧾 Tiquete
    ticket_number = models.CharField(max_length=20, unique=True, verbose_name="Tiquete")
    
    # 📅 Fecha de pesaje
    weighing_date = models.DateTimeField(verbose_name="Fecha de pesaje")

    # NIT del Provedor
    provider_tax_id = models.CharField(max_length=255, verbose_name="NIT Provedor",blank=True, null=True)
    # 📝 Descripción del movimiento
    provider_name = models.CharField(max_length=255, verbose_name="Nombre Provedor", blank=True, null=True)
    
    # 🚛 Vehículo (placa)
    vehicle_id = models.CharField(max_length=20, verbose_name="Vehículo")
    
    # 👨‍✈️ Conductor_id
    driver_name = models.CharField(max_length=100, verbose_name="Conductor")
    
    # 🏡 Driver Name
    driver_id = models.CharField(max_length=100, verbose_name="Nombre del origen o proveedor")

    # ⚖️ Peso Bruto (Kg)
    gross_weight_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Peso Bruto (Kg)")
    
    # ⚖️ Peso Tara (Kg)
    tare_weight_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Peso Tara (Kg)")
    
    # ⚖️ Peso Neto (Kg)
    net_weight_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Peso Neto (Kg)")

    # 🌴 Pedúnculo Largo (PL)
    peduncle_long_units = models.IntegerField(verbose_name="Pedúnculo Largo (Unidades)", blank=True, null=True)
    peduncle_long_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Kilos Pedúnculo Largo (KPL)", blank=True, null=True)

    # 🍌 Racimos Enfermos (RE)
    sick_bunches_units = models.IntegerField(verbose_name="Racimos Enfermos (Unidades)", blank=True, null=True)

    # 🧹 Impurezas (I)
    impurities_units = models.IntegerField(verbose_name="Impurezas (Unidades)", blank=True, null=True)
    impurities_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Kilos Impurezas (KI)", blank=True, null=True)

    # 🧺 Fruta Podrida (RP)
    rotten_fruit_units = models.IntegerField(verbose_name="Fruta Podrida (Unidades)", blank=True, null=True)
    rotten_fruit_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Kilos Fruta Podrida (KRP)", blank=True, null=True)

    # 🍂 Fruta Sobremadura (RSM)
    overripe_fruit_units = models.IntegerField(verbose_name="Fruta Sobremadura (Unidades)", blank=True, null=True)
    overripe_fruit_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Kilos Fruta Sobremadura (KRSM)", blank=True, null=True)

    # 🍈 Fruta Verde (RV)
    green_fruit_units = models.IntegerField(verbose_name="Fruta Verde (Unidades)", blank=True, null=True)
    green_fruit_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Kilos Fruta Verde (KRV)", blank=True, null=True)

    # 🌾 Tusas (T)
    empty_bunches_units = models.IntegerField(verbose_name="Tusas (Unidades)", blank=True, null=True)
    empty_bunches_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Kilos Tusas (KT)", blank=True, null=True)

    # 🟢 Verde con Desprendimiento (VD)
    green_with_detachment_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Verde con Desprendimiento (Kg)", blank=True, null=True)

    # ⚠️ Peso Castigo (Kg)
    penalty_weight_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Peso Castigo (Kg)", blank=True, null=True)
    
    # 💰 A Pagar (Kg)
    payable_weight_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="A Pagar (Kg)", blank=True, null=True)


    class Meta:
        verbose_name = "weight ticket"
        verbose_name_plural = "weight tickets"
        ordering = ["-weighing_date"]
        #app_label = "siipe"

    def __str__(self):
        return f"Tiquete {self.ticket_number} – {self.weighing_date.strftime('%Y-%m-%d')}"

