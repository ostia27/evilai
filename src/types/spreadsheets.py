from typing import Union, Iterable, Any, Optional, MutableMapping

from gspread import Worksheet
from gspread.utils import Dimension, ValueInputOption, ValueRenderOption, DateTimeOption
from gspread.worksheet import JSONResponse


class WorksheetWrapper(Worksheet):

    def batch_update(self, data: Iterable[MutableMapping[str, Any]], raw: bool = True,
                     value_input_option: Optional[ValueInputOption] = None,
                     include_values_in_response: Optional[bool] = None,
                     response_value_render_option: Optional[ValueRenderOption] = None,
                     response_date_time_render_option: Optional[DateTimeOption] = None) -> JSONResponse:
        return super().batch_update(data, raw, value_input_option, include_values_in_response,
                                    response_value_render_option, response_date_time_render_option)