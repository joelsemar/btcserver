# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Table'
        db.create_table('backend_table', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('deck', self.gf('django.db.models.fields.TextField')(default='')),
            ('current_turn', self.gf('django.db.models.fields.related.ForeignKey')(related_name='playing_at', null=True, to=orm['backend.Seat'])),
        ))
        db.send_create_signal('backend', ['Table'])

        # Adding model 'Player'
        db.create_table('backend_player', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('handle', self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True)),
            ('show_animations', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('payout_address', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('account_name', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=512, blank=True)),
        ))
        db.send_create_signal('backend', ['Player'])

        # Adding model 'Card'
        db.create_table('backend_card', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('suite', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('backend', ['Card'])

        # Adding unique constraint on 'Card', fields ['value', 'suite']
        db.create_unique('backend_card', ['value', 'suite'])

        # Adding model 'Seat'
        db.create_table('backend_seat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('table', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Table'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Player'], null=True)),
        ))
        db.send_create_signal('backend', ['Seat'])

        # Adding unique constraint on 'Seat', fields ['table', 'player']
        db.create_unique('backend_seat', ['table_id', 'player_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Seat', fields ['table', 'player']
        db.delete_unique('backend_seat', ['table_id', 'player_id'])

        # Removing unique constraint on 'Card', fields ['value', 'suite']
        db.delete_unique('backend_card', ['value', 'suite'])

        # Deleting model 'Table'
        db.delete_table('backend_table')

        # Deleting model 'Player'
        db.delete_table('backend_player')

        # Deleting model 'Card'
        db.delete_table('backend_card')

        # Deleting model 'Seat'
        db.delete_table('backend_seat')


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['backend']
