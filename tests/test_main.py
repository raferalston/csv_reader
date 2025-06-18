import sys

import pytest

from tabulate import tabulate

from ..main import CSVReader, ValidCommandError, ReuqiredArgumentsError, UnkwnownYetError



class TestProgramExecution:
    @pytest.fixture
    def mock_argv(self, monkeypatch):
        """Fixture to simulate command line arguments"""
        def set_argv(args):
            monkeypatch.setattr(sys, 'argv', ['program_name'] + args)
        return set_argv

    def test_no_data_found(self, mock_argv, capsys):
        """Test filtering by brand"""
        mock_argv(['--file', 'tests/test_example.csv', '--where', 'brand=foo'])
        c = CSVReader()
        c.read()
        captured = capsys.readouterr()
    
        expected_table = tabulate(
            [['No data found']], 
            headers=['No data found'],
            tablefmt='grid',
            numalign='right',
            stralign='left')
        
        assert expected_table in captured.out

    def test_where_equals_correct(self, mock_argv, capsys):
        """Test WHERE"""
        mock_argv(['--file', 'tests/test_example.csv', '--where', 'brand=xiaomi'])
        c = CSVReader()
        c.read()
        captured = capsys.readouterr()
        
        expected_table = tabulate(
            [
                ['redmi note 12', 'xiaomi', '199', '4.6'],
                ['poco x5 pro ', 'xiaomi', '299', '4.4'],
                ], 
            headers=['name', 'brand', 'price', 'rating'],
            tablefmt='grid',
            numalign='right',
            stralign='left')
        
        assert expected_table in captured.out
    
    def test_where_less_correct_data(self, mock_argv, capsys):
        """Test WHERE"""
        mock_argv(['--file', 'tests/test_example.csv', '--where', 'price<300'])
        c = CSVReader()
        c.read()
        captured = capsys.readouterr()
        
        expected_table = tabulate(
            [
                ['redmi note 12', 'xiaomi', '199', '4.6'],
                ['poco x5 pro', 'xiaomi', '299', '4.4'],
                ], 
            headers=['name', 'brand', 'price', 'rating'],
            tablefmt='grid',
            numalign='right',
            stralign='left')
        
        assert expected_table in captured.out
    
    def test_where_greater_correct_data(self, mock_argv, capsys):
        """Test WHERE"""
        mock_argv(['--file', 'tests/test_example.csv', '--where', 'price>300'])
        c = CSVReader()
        c.read()
        captured = capsys.readouterr()
        
        expected_table = tabulate(
            [
                ['iphone 15 pro', 'apple', '999', '4.9'],
                ['galaxy s23 ultra', 'samsung', '1199', '4.8'],
            ], 
            headers=['name', 'brand', 'price', 'rating'],
            tablefmt='grid',
            numalign='right',
            stralign='left')
        
        assert expected_table in captured.out

    def test_where_incorrect_data(self, mock_argv, capsys):
        """Test WHERE"""
        mock_argv(['--file', 'tests/test_example.csv', '--where', 'price>foo'])
        with pytest.raises(ValidCommandError) as exc_info:
            c = CSVReader()
            c.read()
        assert "Check the type - '>' not supported between instances of 'float' and 'str'" in str(exc_info.value)
    
        mock_argv(['--file', 'tests/test_example.csv', '--where', 'foo>15'])
        with pytest.raises(ValidCommandError) as exc_info:
            c = CSVReader()
            c.read()
        assert "Missing parameter - 'foo'" in str(exc_info.value)

        mock_argv(['--file', 'tests/test_example.csv', '--where', 'foo>bar'])
        with pytest.raises(ValidCommandError) as exc_info:
            c = CSVReader()
            c.read()
        assert "Missing parameter - 'foo'" in str(exc_info.value)

    def test_aggregate_avg_correct_data(self, mock_argv, capsys):
        """Test AGGREGATE"""
        mock_argv(['--file', 'tests/test_example.csv', '--aggregate', 'rating=avg'])
        c = CSVReader()
        c.read()
        captured = capsys.readouterr()
        
        expected_table = tabulate(
            [
                ['4.675'],
            ], 
            headers=['avg'],
            tablefmt='grid',
            numalign='right',
            stralign='left')
        
        assert expected_table in captured.out
    
    def test_aggregate_min_correct_data(self, mock_argv, capsys):
        """Test AGGREGATE"""
        mock_argv(['--file', 'tests/test_example.csv', '--aggregate', 'rating=min'])
        c = CSVReader()
        c.read()
        captured = capsys.readouterr()
        
        expected_table = tabulate(
            [
                ['4.4'],
            ], 
            headers=['min'],
            tablefmt='grid',
            numalign='right',
            stralign='left')
        
        assert expected_table in captured.out
    
    def test_aggregate_greater_correct_data(self, mock_argv, capsys):
        """Test AGGREGATE"""
        mock_argv(['--file', 'tests/test_example.csv', '--aggregate', 'rating=max'])
        c = CSVReader()
        c.read()
        captured = capsys.readouterr()
        
        expected_table = tabulate(
            [
                ['4.9'],
            ], 
            headers=['max'],
            tablefmt='grid',
            numalign='right',
            stralign='left')
        
        assert expected_table in captured.out

    def test_where_aggregate_correct_data(self, mock_argv, capsys):
        """Test WHERE and AGGREGATE"""
        mock_argv(['--file', 'tests/test_example.csv', '--where', 'brand=xiaomi', '--aggregate', 'rating=min'])
        c = CSVReader()
        c.read()
        captured = capsys.readouterr()
        
        expected_table = tabulate(
            [
                ['4.4'],
            ], 
            headers=['min'],
            tablefmt='grid',
            numalign='right',
            stralign='left')
        
        assert expected_table in captured.out

    def test_where_aggregate_correct_data_different_positioning(self, mock_argv, capsys):
        """Test WHERE and AGGREGATE"""
        mock_argv(['--file', 'tests/test_example.csv', '--aggregate', 'rating=min', '--where', 'brand=xiaomi'])
        c = CSVReader()
        c.read()
        captured = capsys.readouterr()
        
        expected_table = tabulate(
            [
                ['4.4'],
            ], 
            headers=['min'],
            tablefmt='grid',
            numalign='right',
            stralign='left')
        
        assert expected_table in captured.out

    def test_aggregate_incorrect_data(self, mock_argv, capsys):
        """Test AGGREGATE incorrect data"""
        mock_argv(['--file', 'tests/test_example.csv', '--aggregate', 'price>foo'])
        with pytest.raises(ValidCommandError) as exc_info:
            c = CSVReader()
            c.read()
        assert "Check the type - 'NoneType' object is not callable" in str(exc_info.value)
    
        mock_argv(['--file', 'tests/test_example.csv', '--aggregate', 'foo>min'])
        with pytest.raises(ValidCommandError) as exc_info:
            c = CSVReader()
            c.read()
        assert "Missing parameter - 'foo'" in str(exc_info.value)

        mock_argv(['--file', 'tests/test_example.csv', '--aggregate', 'foo>bar'])
        with pytest.raises(ValidCommandError) as exc_info:
            c = CSVReader()
            c.read()
        assert "Missing parameter - 'foo'" in str(exc_info.value)

    def test_no_file_argument(self, mock_argv, capsys):
        """Test no file argument"""
        mock_argv(['--aggregate', 'rating=avg'])
        with pytest.raises(ReuqiredArgumentsError) as exc_info:
            c = CSVReader()
            c.read()
        assert "Invalid arguments passed" in str(exc_info.value)
    
    def test_wrong_file_name(self, mock_argv, capsys):
        """Test no file name"""
        mock_argv(['--file', 'foo'])
        with pytest.raises(FileNotFoundError) as exc_info:
            c = CSVReader()
            c.read()
        assert "No such file or directory: 'foo'" in str(exc_info.value)

    def test_no_arguments(self, mock_argv, capsys):
        """Test no_argument"""
        mock_argv([])
        with pytest.raises(ReuqiredArgumentsError) as exc_info:
            c = CSVReader()
            c.read()
        assert "Invalid arguments passed" in str(exc_info.value)

    def test_aggregate_no_data_in_file(self, mock_argv, capsys):
        """Test no data in file"""
        mock_argv(['--file', 'tests/test_nodata.csv'])
        c = CSVReader()
        c.read()
        captured = capsys.readouterr()
    
        expected_table = tabulate(
            [['No data found']], 
            headers=['No data found'],
            tablefmt='grid',
            numalign='right',
            stralign='left')
        
        assert expected_table in captured.out