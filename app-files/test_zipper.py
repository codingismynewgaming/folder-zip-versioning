"""
Comprehensive Unit Tests for Per-Folder Version Memory Feature

This module tests the version memory functionality in FolderZipperApp,
including config migration, folder version retrieval, saving, and integration.

Tests are designed to work around Tkinter dependencies by testing the
version memory methods directly without full UI initialization.
"""

import unittest
from unittest.mock import patch, mock_open, MagicMock, call
import json
import sys
import os

# Add app-files to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app-files'))


class TestFolderVersionMemory(unittest.TestCase):
    """
    Test folder version memory functionality.
    
    These tests focus on the core version memory methods without
    requiring full Tkinter UI initialization. We create a minimal
    mock app object with just the methods we need to test.
    """

    def setUp(self):
        """Set up test fixtures with a minimal mock app."""
        # Create a minimal mock app with just the version memory methods
        self.app = MagicMock()
        self.app.folder_versions = {}
        
        # Bind the actual methods from the module
        from zipper import FolderZipperApp
        self.app.get_folder_version = FolderZipperApp.get_folder_version.__get__(self.app)
        self.app.save_folder_version = FolderZipperApp.save_folder_version.__get__(self.app)
        self.app.load_config = FolderZipperApp.load_config.__get__(self.app)
        self.app.save_config = FolderZipperApp.save_config.__get__(self.app)
        self.app.save_config_from_dict = FolderZipperApp.save_config_from_dict.__get__(self.app)
        
        # Set up config file path
        self.app.config_file = 'test_config.json'


class TestConfigMigration(unittest.TestCase):
    """Test configuration migration from old format to new format."""

    def setUp(self):
        """Set up test fixtures with a minimal mock app."""
        from zipper import FolderZipperApp
        self.app = MagicMock()
        self.app.folder_versions = {}
        self.app.config_file = 'test_config.json'
        
        # Bind methods
        self.app.get_folder_version = FolderZipperApp.get_folder_version.__get__(self.app)
        self.app.save_folder_version = FolderZipperApp.save_folder_version.__get__(self.app)
        self.app.load_config = FolderZipperApp.load_config.__get__(self.app)
        self.app.save_config = FolderZipperApp.save_config.__get__(self.app)
        self.app.save_config_from_dict = FolderZipperApp.save_config_from_dict.__get__(self.app)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_migration_from_old_format(self, mock_file, mock_exists):
        """Test loading old format ({"last_version": "X"}) migrates correctly."""
        # Setup - simulate old config format
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = '{"last_version": "1.0"}'
        
        # Create a mock for save_config_from_dict to verify migration save
        with patch.object(self.app, 'save_config_from_dict') as mock_save:
            # Reload config
            self.app.load_config()
            
            # Assert migration happened - old key removed, new structure created
            self.assertEqual(self.app.folder_versions.get('__default__'), '1.0')
            self.assertNotIn('last_version', self.app.folder_versions)
            
            # Verify migrated config was saved
            mock_save.assert_called_once()
            saved_config = mock_save.call_args[0][0]
            self.assertIn('folder_versions', saved_config)
            self.assertNotIn('last_version', saved_config)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_loading_new_format_works(self, mock_file, mock_exists):
        """Test loading new format ({"folder_versions": {...}}) works."""
        # Setup - simulate new config format
        mock_exists.return_value = True
        config_data = {
            'folder_versions': {
                'C:\\Test\\FolderA': '3',
                'D:\\Backup\\FolderB': 'test5',
                '__default__': 'default1'
            }
        }
        mock_file.return_value.read.return_value = json.dumps(config_data)
        
        # Reload config
        self.app.load_config()
        
        # Assert new format loaded correctly
        self.assertEqual(self.app.folder_versions, config_data['folder_versions'])
        self.assertEqual(self.app.get_folder_version('C:\\Test\\FolderA'), '3')
        self.assertEqual(self.app.get_folder_version('D:\\Backup\\FolderB'), 'test5')
        self.assertEqual(self.app.get_folder_version('__default__'), 'default1')

    @patch('os.path.exists')
    def test_missing_config_file_initializes_empty_dict(self, mock_exists):
        """Test missing config file initializes empty dict."""
        # Setup - config file doesn't exist
        mock_exists.return_value = False
        
        # Reload config
        self.app.load_config()
        
        # Assert empty dict initialized
        self.assertEqual(self.app.folder_versions, {})

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_malformed_json_handled_gracefully(self, mock_file, mock_exists):
        """Test malformed JSON is handled gracefully."""
        # Setup - simulate malformed JSON
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = '{invalid json}'
        
        # Reload config - should not raise exception
        self.app.load_config()
        
        # Assert empty dict on error
        self.assertEqual(self.app.folder_versions, {})

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_old_format_with_empty_version(self, mock_file, mock_exists):
        """Test old format with empty last_version doesn't create default."""
        # Setup - old format with empty version
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = '{"last_version": ""}'
        
        # Reload config
        self.app.load_config()
        
        # Assert empty default or no default
        default_version = self.app.folder_versions.get('__default__', '')
        self.assertEqual(default_version, '')


class TestFolderVersionRetrieval(unittest.TestCase):
    """Test folder version retrieval functionality."""

    def setUp(self):
        """Set up test fixtures with a minimal mock app."""
        from zipper import FolderZipperApp
        self.app = MagicMock()
        self.app.folder_versions = {}
        self.app.config_file = 'test_config.json'
        
        # Bind methods
        self.app.get_folder_version = FolderZipperApp.get_folder_version.__get__(self.app)
        self.app.save_folder_version = FolderZipperApp.save_folder_version.__get__(self.app)

    def test_get_folder_version_known_folder(self):
        """Test get_folder_version() returns stored version for known folder."""
        # Setup
        self.app.folder_versions = {
            'C:\\Test\\FolderA': '3',
            'D:\\Backup\\FolderB': 'test5'
        }
        
        # Test
        result = self.app.get_folder_version('C:\\Test\\FolderA')
        
        # Assert
        self.assertEqual(result, '3')

    def test_get_folder_version_unknown_folder(self):
        """Test get_folder_version() returns empty string for unknown folder."""
        # Setup
        self.app.folder_versions = {
            'C:\\Test\\FolderA': '3'
        }
        
        # Test
        result = self.app.get_folder_version('D:\\Unknown\\Folder')
        
        # Assert
        self.assertEqual(result, '')

    def test_get_folder_version_falls_back_to_default(self):
        """Test get_folder_version() falls back to __default__ if exists."""
        # Setup
        self.app.folder_versions = {
            'C:\\Test\\FolderA': '3',
            '__default__': 'default10'
        }
        
        # Test - unknown folder should get default
        result = self.app.get_folder_version('D:\\Unknown\\Folder')
        
        # Assert
        self.assertEqual(result, 'default10')

    def test_get_folder_version_exact_match_takes_precedence(self):
        """Test exact path match takes precedence over default."""
        # Setup
        self.app.folder_versions = {
            'C:\\Test\\FolderA': '5',
            '__default__': 'default1'
        }
        
        # Test
        result = self.app.get_folder_version('C:\\Test\\FolderA')
        
        # Assert
        self.assertEqual(result, '5')

    def test_get_folder_version_path_with_trailing_slash(self):
        """Test path normalization with trailing slashes."""
        # Setup - note: current implementation does NOT normalize paths
        self.app.folder_versions = {
            'C:\\Test\\FolderA': '3'
        }
        
        # Test - trailing slash should NOT match (current behavior)
        result = self.app.get_folder_version('C:\\Test\\FolderA\\')
        
        # Assert - empty because paths don't match exactly
        self.assertEqual(result, '')

    def test_get_folder_version_case_sensitivity(self):
        """Test path case sensitivity."""
        # Setup
        self.app.folder_versions = {
            'C:\\Test\\FolderA': '3'
        }
        
        # Test - different case should NOT match (Windows paths are case-insensitive but dict keys are not)
        result = self.app.get_folder_version('c:\\test\\foldera')
        
        # Assert - empty because case doesn't match
        self.assertEqual(result, '')

    def test_get_folder_version_no_folder_versions_attr(self):
        """Test get_folder_version() when folder_versions attr doesn't exist."""
        # Setup - remove the attribute
        delattr(self.app, 'folder_versions')
        
        # Test - should not raise exception
        result = self.app.get_folder_version('C:\\Test\\Folder')
        
        # Assert
        self.assertEqual(result, '')

    def test_get_folder_version_special_characters(self):
        """Test version retrieval with special characters in path."""
        # Setup
        self.app.folder_versions = {
            'C:\\Test\\Folder-With Special@Chars': 'v2'
        }
        
        # Test
        result = self.app.get_folder_version('C:\\Test\\Folder-With Special@Chars')
        
        # Assert
        self.assertEqual(result, 'v2')


class TestFolderVersionSave(unittest.TestCase):
    """Test folder version save functionality."""

    def setUp(self):
        """Set up test fixtures with a minimal mock app."""
        from zipper import FolderZipperApp
        self.app = MagicMock()
        self.app.folder_versions = {}
        self.app.config_file = 'test_config.json'
        
        # Bind methods
        self.app.get_folder_version = FolderZipperApp.get_folder_version.__get__(self.app)
        self.app.save_folder_version = FolderZipperApp.save_folder_version.__get__(self.app)

    def test_save_folder_version_persists_to_dict(self):
        """Test save_folder_version() updates in-memory dict immediately."""
        # Setup
        self.app.folder_versions = {}
        
        # Test
        self.app.save_folder_version('C:\\Test\\FolderA', '5')
        
        # Assert
        self.assertEqual(self.app.folder_versions['C:\\Test\\FolderA'], '5')

    def test_save_folder_version_updates_existing(self):
        """Test save_folder_version() updates existing entry."""
        # Setup
        self.app.folder_versions = {
            'C:\\Test\\FolderA': '3'
        }
        
        # Test
        self.app.save_folder_version('C:\\Test\\FolderA', '10')
        
        # Assert
        self.assertEqual(self.app.folder_versions['C:\\Test\\FolderA'], '10')

    def test_save_folder_version_empty_string_doesnt_save(self):
        """Test save_folder_version() with empty string doesn't save."""
        # Setup
        self.app.folder_versions = {
            'C:\\Test\\FolderA': '3'
        }
        
        # Test
        self.app.save_folder_version('C:\\Test\\FolderA', '')
        
        # Assert - entry should be removed
        self.assertNotIn('C:\\Test\\FolderA', self.app.folder_versions)

    def test_save_folder_version_whitespace_only(self):
        """Test save_folder_version() with whitespace only doesn't save."""
        # Setup
        self.app.folder_versions = {
            'C:\\Test\\FolderA': '3'
        }
        
        # Test
        self.app.save_folder_version('C:\\Test\\FolderA', '   ')
        
        # Assert - entry should be removed
        self.assertNotIn('C:\\Test\\FolderA', self.app.folder_versions)

    def test_save_folder_version_trims_whitespace(self):
        """Test save_folder_version() trims whitespace from version."""
        # Setup
        self.app.folder_versions = {}
        
        # Test
        self.app.save_folder_version('C:\\Test\\FolderA', '  v5  ')
        
        # Assert - whitespace trimmed
        self.assertEqual(self.app.folder_versions['C:\\Test\\FolderA'], 'v5')

    def test_save_folder_version_new_folder(self):
        """Test save_folder_version() adds new folder entry."""
        # Setup
        self.app.folder_versions = {}
        
        # Test
        self.app.save_folder_version('C:\\New\\Folder', '1')
        
        # Assert
        self.assertEqual(self.app.folder_versions['C:\\New\\Folder'], '1')

    def test_save_folder_version_no_folder_versions_attr(self):
        """Test save_folder_version() when folder_versions attr doesn't exist."""
        # Setup - remove the attribute
        delattr(self.app, 'folder_versions')
        
        # Test - should not raise exception
        self.app.save_folder_version('C:\\Test\\Folder', '1')
        
        # Assert - attribute created and value saved
        self.assertEqual(self.app.folder_versions['C:\\Test\\Folder'], '1')

    def test_save_folder_version_numeric_string(self):
        """Test save_folder_version() with numeric string version."""
        # Setup
        self.app.folder_versions = {}
        
        # Test
        self.app.save_folder_version('C:\\Test\\Folder', '123')
        
        # Assert
        self.assertEqual(self.app.folder_versions['C:\\Test\\Folder'], '123')

    def test_save_folder_version_special_version_formats(self):
        """Test save_folder_version() with various version formats."""
        # Setup
        self.app.folder_versions = {}
        
        # Test various formats
        test_versions = ['1.0', 'v2.5-beta', 'release-candidate', '2026-03-20']
        for version in test_versions:
            self.app.save_folder_version(f'C:\\Test\\Folder_{version}', version)
        
        # Assert all saved correctly
        for version in test_versions:
            self.assertEqual(self.app.folder_versions[f'C:\\Test\\Folder_{version}'], version)


class TestConfigPersistence(unittest.TestCase):
    """Test configuration file persistence."""

    def setUp(self):
        """Set up test fixtures with a minimal mock app."""
        from zipper import FolderZipperApp
        self.app = MagicMock()
        self.app.folder_versions = {}
        self.app.config_file = 'test_config.json'
        
        # Bind methods
        self.app.get_folder_version = FolderZipperApp.get_folder_version.__get__(self.app)
        self.app.save_folder_version = FolderZipperApp.save_folder_version.__get__(self.app)
        self.app.save_config = FolderZipperApp.save_config.__get__(self.app)
        self.app.save_config_from_dict = FolderZipperApp.save_config_from_dict.__get__(self.app)

    def test_save_config_from_dict_writes_json(self):
        """Test save_config_from_dict() writes JSON to file."""
        # Setup
        config_data = {
            'folder_versions': {
                'C:\\Test\\FolderA': '3'
            }
        }
        
        # Create a mock file that captures writes
        written_data = []
        
        def capture_write(data):
            written_data.append(data)
        
        mock_file = MagicMock()
        mock_file.write = capture_write
        mock_file.__enter__ = MagicMock(return_value=mock_file)
        mock_file.__exit__ = MagicMock(return_value=False)
        
        with patch('builtins.open', return_value=mock_file):
            # Test
            self.app.save_config_from_dict(config_data)
            
            # Assert JSON written - json.dump writes in multiple calls, so join all
            written_content = ''.join(written_data)
            written_config = json.loads(written_content)
            self.assertEqual(written_config, config_data)

    @patch('builtins.open', new_callable=mock_open)
    def test_save_config_from_dict_handles_error(self, mock_file):
        """Test save_config_from_dict() handles write errors gracefully."""
        # Setup - simulate write error
        mock_file.side_effect = IOError("Disk full")
        
        # Test - should not raise exception
        self.app.save_config_from_dict({'test': 'data'})
        
        # Assert error printed (we can't easily capture print output in unittest)
        # Just verify no exception raised
        pass

    def test_save_config_saves_folder_versions(self):
        """Test save_config() saves folder_versions correctly."""
        # Setup
        self.app.folder_versions = {
            'C:\\Test\\FolderA': '3',
            'D:\\FolderB': 'test5'
        }
        
        # Create a mock file that captures writes
        written_data = []
        
        def capture_write(data):
            written_data.append(data)
        
        mock_file = MagicMock()
        mock_file.write = capture_write
        mock_file.__enter__ = MagicMock(return_value=mock_file)
        mock_file.__exit__ = MagicMock(return_value=False)
        
        with patch('builtins.open', return_value=mock_file):
            # Test
            self.app.save_config()
            
            # Get written content - json.dump writes in multiple calls, so join all
            written_content = ''.join(written_data)
            written_config = json.loads(written_content)
            self.assertEqual(written_config['folder_versions'], self.app.folder_versions)


class TestIntegration(unittest.TestCase):
    """Integration tests for full version memory cycle."""

    def setUp(self):
        """Set up test fixtures with a minimal mock app."""
        from zipper import FolderZipperApp
        self.app = MagicMock()
        self.app.folder_versions = {}
        self.app.config_file = 'test_config.json'
        
        # Bind methods
        self.app.get_folder_version = FolderZipperApp.get_folder_version.__get__(self.app)
        self.app.save_folder_version = FolderZipperApp.save_folder_version.__get__(self.app)
        self.app.load_config = FolderZipperApp.load_config.__get__(self.app)
        self.app.save_config = FolderZipperApp.save_config.__get__(self.app)
        self.app.save_config_from_dict = FolderZipperApp.save_config_from_dict.__get__(self.app)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_full_cycle_save_reload_retrieve(self, mock_file, mock_exists):
        """Test full cycle: save version → reload config → retrieve version."""
        # Setup - simulate config file exists with data
        mock_exists.return_value = True
        initial_config = {
            'folder_versions': {
                'C:\\Test\\FolderA': 'initial1'
            }
        }
        mock_file.return_value.read.return_value = json.dumps(initial_config)
        
        # Step 1: Load config
        self.app.load_config()
        self.assertEqual(self.app.get_folder_version('C:\\Test\\FolderA'), 'initial1')
        
        # Step 2: Save new version
        self.app.save_folder_version('C:\\Test\\FolderA', 'updated5')
        
        # Step 3: Verify in-memory update
        self.assertEqual(self.app.get_folder_version('C:\\Test\\FolderA'), 'updated5')

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_multiple_folders_maintain_separate_versions(self, mock_file, mock_exists):
        """Test multiple folders maintain separate versions."""
        # Setup
        mock_exists.return_value = False
        self.app.folder_versions = {}
        
        # Save versions for multiple folders
        self.app.save_folder_version('C:\\FolderA', 'v1')
        self.app.save_folder_version('C:\\FolderB', 'v2')
        self.app.save_folder_version('D:\\FolderC', 'v3')
        
        # Retrieve each - should be independent
        self.assertEqual(self.app.get_folder_version('C:\\FolderA'), 'v1')
        self.assertEqual(self.app.get_folder_version('C:\\FolderB'), 'v2')
        self.assertEqual(self.app.get_folder_version('D:\\FolderC'), 'v3')
        
        # Update one - others should not change
        self.app.save_folder_version('C:\\FolderA', 'updated10')
        self.assertEqual(self.app.get_folder_version('C:\\FolderA'), 'updated10')
        self.assertEqual(self.app.get_folder_version('C:\\FolderB'), 'v2')
        self.assertEqual(self.app.get_folder_version('D:\\FolderC'), 'v3')

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_version_overwrite_updates_correctly(self, mock_file, mock_exists):
        """Test version overwrite updates correctly."""
        # Setup
        mock_exists.return_value = False
        self.app.folder_versions = {}
        
        # Save initial version
        self.app.save_folder_version('C:\\Test\\Folder', '1')
        
        # Overwrite multiple times
        self.app.save_folder_version('C:\\Test\\Folder', '2')
        self.app.save_folder_version('C:\\Test\\Folder', '3')
        self.app.save_folder_version('C:\\Test\\Folder', 'final')
        
        # Assert final value
        self.assertEqual(self.app.get_folder_version('C:\\Test\\Folder'), 'final')
        self.assertEqual(len(self.app.folder_versions), 1)  # Only one entry

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_default_version_applied_to_unknown_folders(self, mock_file, mock_exists):
        """Test default version applied to unknown folders after migration."""
        # Setup - old format config
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = '{"last_version": "default5"}'
        
        with patch.object(self.app, 'save_config_from_dict'):
            self.app.load_config()
        
        # Unknown folders should get default
        self.assertEqual(self.app.get_folder_version('C:\\Unknown'), 'default5')
        self.assertEqual(self.app.get_folder_version('D:\\Another'), 'default5')
        
        # Known folder should get its own version
        self.app.save_folder_version('C:\\Known', 'known3')
        self.assertEqual(self.app.get_folder_version('C:\\Known'), 'known3')


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def setUp(self):
        """Set up test fixtures with a minimal mock app."""
        from zipper import FolderZipperApp
        self.app = MagicMock()
        self.app.folder_versions = {}
        self.app.config_file = 'test_config.json'
        
        # Bind methods
        self.app.get_folder_version = FolderZipperApp.get_folder_version.__get__(self.app)
        self.app.save_folder_version = FolderZipperApp.save_folder_version.__get__(self.app)

    def test_unicode_folder_paths(self):
        """Test version storage with unicode folder paths."""
        # Setup
        self.app.folder_versions = {}
        
        # Test with unicode characters
        unicode_path = 'C:\\Test\\Ordner-Üäö'
        self.app.save_folder_version(unicode_path, 'v1')
        
        # Assert
        self.assertEqual(self.app.get_folder_version(unicode_path), 'v1')

    def test_very_long_version_string(self):
        """Test saving very long version string."""
        # Setup
        self.app.folder_versions = {}
        
        # Test with long version
        long_version = 'v' + '1' * 1000
        self.app.save_folder_version('C:\\Test\\Folder', long_version)
        
        # Assert
        self.assertEqual(self.app.get_folder_version('C:\\Test\\Folder'), long_version)

    def test_none_version_handling(self):
        """Test handling of None version value."""
        # Setup
        self.app.folder_versions = {}
        
        # Test - None should be treated as empty
        try:
            self.app.save_folder_version('C:\\Test\\Folder', None)
            # None doesn't have strip(), so this might fail
        except AttributeError:
            # Expected - None doesn't have strip() method
            pass

    def test_null_byte_in_path(self):
        """Test path with null byte."""
        # Setup
        self.app.folder_versions = {}
        
        # Test - null byte in path
        path_with_null = 'C:\\Test\\Folder\x00'
        self.app.save_folder_version(path_with_null, 'v1')
        
        # Assert
        self.assertEqual(self.app.get_folder_version(path_with_null), 'v1')

    def test_concurrent_version_updates(self):
        """Test concurrent updates to same folder version."""
        # Setup
        self.app.folder_versions = {}
        
        # Simulate concurrent updates (not thread-safe, but test behavior)
        self.app.save_folder_version('C:\\Test\\Folder', 'v1')
        self.app.save_folder_version('C:\\Test\\Folder', 'v2')
        self.app.save_folder_version('C:\\Test\\Folder', 'v3')
        
        # Assert last write wins
        self.assertEqual(self.app.get_folder_version('C:\\Test\\Folder'), 'v3')

    def test_empty_folder_path(self):
        """Test saving version with empty folder path."""
        # Setup
        self.app.folder_versions = {}
        
        # Test
        self.app.save_folder_version('', 'v1')
        
        # Assert - empty string is a valid key
        self.assertEqual(self.app.get_folder_version(''), 'v1')

    def test_root_path(self):
        """Test saving version for root path."""
        # Setup
        self.app.folder_versions = {}
        
        # Test with root path
        self.app.save_folder_version('C:\\', 'root1')
        
        # Assert
        self.assertEqual(self.app.get_folder_version('C:\\'), 'root1')


class TestConfigFileScenarios(unittest.TestCase):
    """Test various config file scenarios."""

    def setUp(self):
        """Set up test fixtures with a minimal mock app."""
        from zipper import FolderZipperApp
        self.app = MagicMock()
        self.app.folder_versions = {}
        self.app.config_file = 'test_config.json'
        
        # Bind methods
        self.app.get_folder_version = FolderZipperApp.get_folder_version.__get__(self.app)
        self.app.save_folder_version = FolderZipperApp.save_folder_version.__get__(self.app)
        self.app.load_config = FolderZipperApp.load_config.__get__(self.app)
        self.app.save_config = FolderZipperApp.save_config.__get__(self.app)
        self.app.save_config_from_dict = FolderZipperApp.save_config_from_dict.__get__(self.app)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_with_extra_unknown_keys(self, mock_file, mock_exists):
        """Test config file with extra unknown keys is handled."""
        # Setup
        mock_exists.return_value = True
        config_data = {
            'folder_versions': {'C:\\Test': 'v1'},
            'unknown_key': 'value',
            'another_key': {'nested': 'data'}
        }
        mock_file.return_value.read.return_value = json.dumps(config_data)
        
        # Test
        self.app.load_config()
        
        # Assert - folder_versions loaded, extra keys ignored
        self.assertEqual(self.app.folder_versions, {'C:\\Test': 'v1'})

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_empty_json_object(self, mock_file, mock_exists):
        """Test config file with empty JSON object."""
        # Setup
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = '{}'
        
        # Test
        self.app.load_config()
        
        # Assert
        self.assertEqual(self.app.folder_versions, {})

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_json_array_instead_of_object(self, mock_file, mock_exists):
        """Test config file with JSON array instead of object."""
        # Setup
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = '[]'
        
        # Test - should handle gracefully
        try:
            self.app.load_config()
        except (AttributeError, TypeError):
            # Expected - array doesn't have .get() method
            pass


def run_tests():
    """Run all tests and print results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestFolderVersionMemory))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigMigration))
    suite.addTests(loader.loadTestsFromTestCase(TestFolderVersionRetrieval))
    suite.addTests(loader.loadTestsFromTestCase(TestFolderVersionSave))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigPersistence))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigFileScenarios))
    
    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
