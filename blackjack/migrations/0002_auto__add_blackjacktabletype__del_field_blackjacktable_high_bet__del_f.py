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
            ('low_bet', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('high_bet', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal('blackjack', ['BlackJackTableType'])

        # Deleting field 'BlackJackTable.high_bet'
        db.delete_column('blackjack_blackjacktable', 'high_bet')

        # Deleting field 'BlackJackTable.low_bet'
        db.delete_column('blackjack_blackjacktable', 'low_bet')

        # Adding field 'BlackJackTable.type'
        db.add_column('blackjack_blackjacktable', 'type', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['blackjack.BlackJackTableType']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'BlackJackTableType'
        db.delete_table('blackjack_blackjacktabletype')

        # We cannot add back in field 'BlackJackTable.high_bet'
        raise RuntimeError(
            "Cannot reverse this migration. 'BlackJackTable.high_bet' and its values cannot be restored.")

        # We cannot add back in field 'BlackJackTable.low_bet'
        raise RuntimeError(
            "Cannot reverse this migration. 'BlackJackTable.low_bet' and its values cannot be restored.")

        # Deleting field 'BlackJackTable.type'
        db.delete_column('blackjack_blackjacktable', 'type_id')


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
            'payout_address': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'show_animations': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'backend.table': {
            'Meta': {'object_name': 'Table'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'blackjack.blackjackbet': {
            'Meta': {'object_name': 'BlackJackBet'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blackjack.BlackJackRound']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.Player']"}),
            'players_hand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blackjack.BlackJackHand']"}),
            'score': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'blackjack.blackjackhand': {
            'Meta': {'object_name': 'BlackJackHand'},
            'cards': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['backend.Card']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'blackjack.blackjackround': {
            'Meta': {'object_name': 'BlackJackRound'},
            'dealers_hand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blackjack.BlackJackHand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'table': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blackjack.BlackJackTable']"})
        },
        'blackjack.blackjacktable': {
            'Meta': {'object_name': 'BlackJackTable', '_ormbases': ['backend.Table']},
            'table_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['backend.Table']", 'unique': 'True', 'primary_key': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blackjack.BlackJackTableType']"})
        },
        'blackjack.blackjacktabletype': {
            'Meta': {'object_name': 'BlackJackTableType'},
            'high_bet': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'low_bet': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
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
