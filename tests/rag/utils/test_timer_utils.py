import pytest
import time
from rag.utils import timer_utils

def test_now():
    t1 = timer_utils.now()
    time.sleep(0.01) # Sleep 10ms
    t2 = timer_utils.now()
    
    assert t2 > t1
    assert isinstance(t1, int)
