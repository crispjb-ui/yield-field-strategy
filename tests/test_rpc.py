from yf.rpc import selector, enc_addr, enc_uint

def test_selectors_match_known_values():
    assert selector("balanceOf(address)") == "0x70a08231"
    assert selector("ownerOf(uint256)") == "0x6352211e"
    assert selector("decimals()") == "0x313ce567"
    assert selector("transfer(address,uint256)") == "0xa9059cbb"

def test_encoders():
    assert enc_uint(1) == "0" * 63 + "1"
    assert enc_addr("0xAbC") == "0" * 61 + "abc"
