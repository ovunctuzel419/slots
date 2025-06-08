import time
import csv
from typing import Dict, List

import attrs
from attrs import define


@define
class CSVReader:
    _cache: Dict[str, List[List[str]]] = attrs.field(factory=dict)

    def read_lines(self, csv_path: str, skip_header: bool = True) -> List[List[str]]:
        if csv_path in self._cache:
            rows = self._cache[csv_path]
        else:
            rows = [row for row in csv.reader(open(csv_path)) if len(row) > 0]
            self._cache[csv_path] = rows
        return rows if not skip_header else rows[1:]
