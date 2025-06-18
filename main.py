# https://docs.google.com/document/d/1nraUeVCkbsyvjNvMAWAwgrn7w3DXHsQf15QS1eZ2F1U/edit?tab=t.0

import argparse
import csv
import re

from tabulate import tabulate


class UnkwnownYetError(Exception):
    """Exception raised when unexpected Error is occured. 
    Check aggregation_check for further debug.

    Attributes:
        message -- Explanation of the error
    """

    def __init__(self, message: str = 'Check aggregation_check method for futher debug'):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        error_msg = f"{self.message}"
        return error_msg
    

class ValidCommandError(Exception):
    """Exception raised when an invalid command is provided.

    Attributes:
        command -- The invalid command that was input
        message -- Explanation of the error
    """
    def __init__(self, command: str, message: str = 'Invalid command pattern, correct is - "command=parameter"'):
        self.command = command
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        error_msg = f"{self.command} - {self.message}"
        return error_msg


class ReuqiredArgumentsError(Exception):
    """Exception raised when less then needed arguments is passing.

    Attributes:
        command -- list of possible commands
        message -- Explanation of the error
    """
    def __init__(self, command: str, message: str = 'Invalid arguments passed, possible list'):
        self.command = command
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        error_msg = f"{self.message} - [{', '.join(self.command)}]"
        return error_msg


# Helper aggregate functions
def avg(data: list) -> float:
    '''Average aggregation helper function'''
    return sum(data) / len(data) if data else 0


class CSVReader:
    def __init__(self):
        '''Map of possible aggregation methods. Linked with name: func'''
        self.methods_map = {
            'where': self.where,
            'aggregate': self.aggregate,
            }

    def add_aggregation(self, name, func):
        '''Method for adding new aggregation methods.
        This methods need to be in a class, and be wrapped by @aggregation_check'''
        if name not in self.methods_map:
            self.methods_map[name] = func
            print(f'Successed added new method - {name}, with - {func.__name__}')
        else:
            print(f'Method name - {name}, already exists. To change use a set_aggregation(name, func)')

    def set_aggregation(self, name, func):
        '''Method for seting egisting aggregation method.
        This method need to be in a class, and be wrapped by @aggregation_check'''
        if name in self.methods_map:
            self.methods_map[name] = func
            print(f'Successed change method - {name}, with - {func.__name__}')
        else:
            print(f'Method name - {name}, already not exists. To add use a add_aggregation(name, func)')

    def aggregation_check(func):
        '''Error handling for data aggregation'''
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
            except KeyError as e:
                raise ValidCommandError('Missing parameter', str(e))
            except TypeError as e:
                raise ValidCommandError('Wrong data to compare. Check the type', str(e))
            except:
                raise UnkwnownYetError
            return result
        return wrapper
    
    @aggregation_check
    def where(self, data: list, column: str, parameter: str, operator: str = None) -> list:
        '''WHERE filter'''
        if operator == '=':
            return [d for d in data if d[column] == parameter]
        
        if operator == '>':
            return [d for d in data if d[column] > parameter]
        
        if operator == '<':
            return [d for d in data if d[column] < parameter]

    @aggregation_check    
    def aggregate(self, data: list, column: str, parameter: str, operator: str = None) -> list:
        '''AGGREGATE filter'''
        operations = {
            'avg': avg,
            'min': min,
            'max': max,
        }
        data = [value[column] for value in data]
        return [{parameter: operations.get(parameter)(data)}]
    
    def is_number(self, s: str) -> bool:
        '''Helper function for understanding type of data'''
        try:
            float(s)
            return True
        except ValueError:
            return False
        
    def finalize_data(self, commands: dict, data: list) -> None:
        '''Using existing processing commands'''
        for command in self.methods_map:
            # Checks if commands exists
            if not commands.get(command) or not command in commands:
                continue
            col, operator, par = self.parse_command(commands[command])
            data = self.methods_map[command](data, col, par, operator)
        self.print_results(data)

    def print_results(self, data: list) -> None:
        '''Printing final results'''
        if not data:
            print(tabulate(
                [['No data found']],
                headers=['No data found'],
                tablefmt='grid',
                numalign='right',
                stralign='left'
                ))
            return 
        headers = list(next(iter(data)).keys()) # Getting first row data
        table_data = [
            list(d.values()) for d in data
        ]

        print(tabulate(
            table_data,
            headers=headers,
            tablefmt='grid', 
            numalign='right',
            stralign='left'
            ))

    def parse_command(self, command: str) -> tuple:
        '''Parsing commands given. Example: foo>bar -> col='foo', operator='>', par='bar' '''
        pattern = r'(.*?)([^a-zA-Z0-9\s])(.*)'
        match = re.match(pattern, command)
        if match:
            col, operator, par = [part.strip() for part in match.groups()]
            if self.is_number(par):
                par = float(par)
            return col, operator, par
        raise ValidCommandError(command=command)

    def parse_data_from_file(self, filename: str) -> list:
        '''Parsing data from a file'''
        data = []
        if not filename:
            raise ReuqiredArgumentsError(['Missing required --file'])
        with open(filename, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append({
                    column: float(data) if self.is_number(data) else data for column, data in row.items() 
                })
        return data if data else self.print_results(data)

    def command_manager(self, commands: dict) -> None:
        '''Parsing data from a file and running its processing using finalize data'''
        if commands and 'file' in commands:
            data = self.parse_data_from_file(commands['file'])
            if data:
                self.finalize_data(commands, data)
            
    def read(self) -> None:
        '''Entry point to the program. Checks the arguments passed.'''
        parser = argparse.ArgumentParser(description='CSV aggregator')
        parser.add_argument('--file', help='Required argument file link')
        parser.allow_abbrev = False

        for command in self.methods_map:
            parser.add_argument(f'--{command}')

        args, unknown = parser.parse_known_args()
        args = vars(args)

        args_count = sum(1 for arg in args.values() if arg)
        if args_count <= 1 and unknown:
            raise ReuqiredArgumentsError(self.methods_map.keys())
        
        self.command_manager(args)
    

if __name__ == '__main__':
    c = CSVReader()
    c.read()