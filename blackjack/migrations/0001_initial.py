# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'BlackJackTableType'
        db.create_table('blackjack_blackjacktabletype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('low_bet', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=8)),
            ('high_bet', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=8)),
        ))
        db.send_create_signal('blackjack', ['BlackJackTableType'])

        # Adding model 'BlackJackTable'
        db.create_table('blackjack_blackjacktable', (
            ('table_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['backend.Table'], unique=True, primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blackjack.BlackJackTableType'])),
        ))
        db.send_create_signal('blackjack', ['BlackJackTable'])

        # Adding model 'BlackJackRound'
        db.create_table('blackjack_blackjackround', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('table', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blackjack.BlackJackTable'])),
            ('taking_bets', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('blackjack', ['BlackJackRound'])

        # Adding model 'BlackJackHand'
        db.create_table('blackjack_blackjackhand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bet', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=8)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Player'], null=True)),
            ('round', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blackjack.BlackJackRound'])),
            ('dealers_hand', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('blackjack', ['BlackJackHand'])

        # Adding M2M table for field cards on 'BlackJackHand'
        db.create_table('blackjack_blackjackhand_cards', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('blackjackhand', models.ForeignKey(orm['blackjack.blackjackhand'], null=False)),
            ('card', models.ForeignKey(orm['backend.card'], null=False))
        ))
        db.create_unique('blackjack_blackjackhand_cards', ['blackjackhand_id', 'card_id'])


    def backwards(self, orm):
        
        # Deleting model 'BlackJackTableType'
        db.delete_table('blackjack_blackjacktabletype')

        # Deleting model 'BlackJackTable'
        db.delete_table('blackjack_blackjacktable')

        # Deleting model 'BlackJackRound'
        db.delete_table('blackjack_blackjackround')

        # Deleting model 'BlackJackHand'
        db.delete_table('blackjack_blackjackhand')

        # Removing M2M table for field cards on 'BlackJackHand'
        db.delete_table('blackjack_blackjackhand_cards')


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
            'Meta': {'unique_together': "(('value', 'suite'),)", 'object_name': 'Card'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'suite': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'backend.player': {
            'Meta': {'object_name': 'Player'},
            'account_name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '512', 'blank': 'True'}),
            'handle': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payout_address': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'show_animations': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'backend.seat': {
            'Meta': {'unique_together': "(('table', 'player'),)", 'object_name': 'Seat'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.Player']", 'null': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'table': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.Table']"})
        },
        'backend.table': {
            'Meta': {'object_name': 'Table'},
            'current_turn': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'playing_at'", 'null': 'True', 'to': "orm['backend.Seat']"}),
            'deck': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'blackjack.blackjackhand': {
            'Meta': {'object_name': 'BlackJackHand'},
            'bet': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '8'}),
            'cards': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['backend.Card']", 'symmetrical': 'False'}),
            'dealers_hand': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.Player']", 'null': 'True'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blackjack.BlackJackRound']"})
        },
        'blackjack.blackjackround': {
            'Meta': {'object_name': 'BlackJackRound'},
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'table': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blackjack.BlackJackTable']"}),
            'taking_bets': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'blackjack.blackjacktable': {
            'Meta': {'object_name': 'BlackJackTable', '_ormbases': ['backend.Table']},
            'table_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['backend.Table']", 'unique': 'True', 'primary_key': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blackjack.BlackJackTableType']"})
        },
        'blackjack.blackjacktabletype': {
            'Meta': {'object_name': 'BlackJackTableType'},
            'high_bet': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'low_bet': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '8'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['blackjack']
