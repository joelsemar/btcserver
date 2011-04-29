# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'BlackJackTable'
        db.create_table('btcblackjack_blackjacktable', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('low_bet', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('high_bet', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal('btcblackjack', ['BlackJackTable'])

        # Adding model 'Seat'
        db.create_table('btcblackjack_seat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('table', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['btcblackjack.BlackJackTable'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Player'], null=True)),
        ))
        db.send_create_signal('btcblackjack', ['Seat'])

        # Adding model 'Hand'
        db.create_table('btcblackjack_hand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('btcblackjack', ['Hand'])

        # Adding M2M table for field cards on 'Hand'
        db.create_table('btcblackjack_hand_cards', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hand', models.ForeignKey(orm['btcblackjack.hand'], null=False)),
            ('card', models.ForeignKey(orm['backend.card'], null=False))
        ))
        db.create_unique('btcblackjack_hand_cards', ['hand_id', 'card_id'])

        # Adding model 'Round'
        db.create_table('btcblackjack_round', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('table', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['btcblackjack.BlackJackTable'])),
            ('dealers_hand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['btcblackjack.Hand'])),
        ))
        db.send_create_signal('btcblackjack', ['Round'])

        # Adding model 'Bet'
        db.create_table('btcblackjack_bet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['btcblackjack.Round'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('players_hand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['btcblackjack.Hand'])),
            ('score', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Player'])),
        ))
        db.send_create_signal('btcblackjack', ['Bet'])


    def backwards(self, orm):
        
        # Deleting model 'BlackJackTable'
        db.delete_table('btcblackjack_blackjacktable')

        # Deleting model 'Seat'
        db.delete_table('btcblackjack_seat')

        # Deleting model 'Hand'
        db.delete_table('btcblackjack_hand')

        # Removing M2M table for field cards on 'Hand'
        db.delete_table('btcblackjack_hand_cards')

        # Deleting model 'Round'
        db.delete_table('btcblackjack_round')

        # Deleting model 'Bet'
        db.delete_table('btcblackjack_bet')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'backend.card': {
            'Meta': {'object_name': 'Card'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'value': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'backend.player': {
            'Meta': {'object_name': 'Player'},
            'account_name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '512', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payout_address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'show_animations': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'btcblackjack.bet': {
            'Meta': {'object_name': 'Bet'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['btcblackjack.Round']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.Player']"}),
            'players_hand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['btcblackjack.Hand']"}),
            'score': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'btcblackjack.blackjacktable': {
            'Meta': {'object_name': 'BlackJackTable'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'high_bet': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'low_bet': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'btcblackjack.hand': {
            'Meta': {'object_name': 'Hand'},
            'cards': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['backend.Card']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'btcblackjack.round': {
            'Meta': {'object_name': 'Round'},
            'dealers_hand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['btcblackjack.Hand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'table': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['btcblackjack.BlackJackTable']"})
        },
        'btcblackjack.seat': {
            'Meta': {'object_name': 'Seat'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.Player']", 'null': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'table': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['btcblackjack.BlackJackTable']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['btcblackjack']
