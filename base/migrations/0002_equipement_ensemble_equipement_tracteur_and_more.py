# Generated by Django 4.0.3 on 2022-03-24 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipement',
            name='ensemble',
            field=models.CharField(choices=[('porteur', 'Porteur'), ('tracteur', 'Tracteur'), ('remorque', 'Remorque')], default='tracteur', max_length=10, verbose_name='Ensemble'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='equipement',
            name='tracteur',
            field=models.ForeignKey(blank=True, limit_choices_to={'actif': True, 'ensemble': 'tracteur'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='remorques', to='base.equipement', verbose_name='Tracteur'),
        ),
        migrations.AddField(
            model_name='historicalequipement',
            name='ensemble',
            field=models.CharField(choices=[('porteur', 'Porteur'), ('tracteur', 'Tracteur'), ('remorque', 'Remorque')], default='tracteur', max_length=10, verbose_name='Ensemble'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalequipement',
            name='tracteur',
            field=models.ForeignKey(blank=True, db_constraint=False, limit_choices_to={'actif': True, 'ensemble': 'tracteur'}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='base.equipement', verbose_name='Tracteur'),
        ),
    ]
