*** Settings ***
Documentation     This is a resource file, that can contain variables and keywords.
...               Keywords defined here can be used where this Keywords.resource in loaded.
Library           CustomLibrary.py


*** Keywords ***
Clone Source Code
    ${return_code}=    Clone    https://github.com/liuw1/td-shim.git    td-shim
    Should Be Equal    ${return_code}    ${0}
    ${return_code}=    Submodule Init
    Should Be Equal    ${return_code}    ${0}
    ${return_code}=    Apply Patch
    Should Be Equal    ${return_code}    ${0}

Get version 
    [Return]
    ${version_hash}=    Get Git Hash
    Should Not Be Empty    ${version_hash}

Build Final Binary
    [Arguments]    ${item}
    ${return_code}=    Build    ${item}
    Should Be Equal    ${return_code}    ${0}

Run Integration Test
    [Arguments]    ${cpus}    ${mem}    ${firmware}
    ${return_code}=    Integration Test    ${cpus}    ${mem}    ${firmware}
    Should Be Equal    ${return_code}    ${0}

Afl
    [Arguments]    ${time}
    ${return_code}=    Afl Test    afl_elf    ${time}
    Should Be Equal    ${return_code}    ${0}
    ${return_code}=    Afl Test    afl_pe    ${time}
    Should Be Equal    ${return_code}    ${0}
    ${return_code}=    Afl Test    afl_cfv_parser    ${time}
    Should Be Equal    ${return_code}    ${0}
    ${return_code}=    Afl Test    afl_hob_parser    ${time}
    Should Be Equal    ${return_code}    ${0}
    ${return_code}=    Afl Test    afl_payload_parser    ${time}
    Should Be Equal    ${return_code}    ${0}
    ${return_code}=    Afl Test    afl_secure_boot_cfv    ${time}
    Should Be Equal    ${return_code}    ${0}
    ${return_code}=    Afl Test    afl_secure_boot_payload    ${time}
    Should Be Equal    ${return_code}    ${0}

Libfuzzer
    [Arguments]    ${time}
    ${return_code}=    Libfuzzer Test    elf    ${time}
    Should Be Equal    ${return_code}    ${0}
    ${return_code}=    Libfuzzer Test    pe    ${time}
    Should Be Equal    ${return_code}    ${0}
    ${return_code}=    Libfuzzer Test    cfv_parser    ${time}
    Should Be Equal    ${return_code}    ${0}
    ${return_code}=    Libfuzzer Test    hob_parser    ${time}
    Should Be Equal    ${return_code}    ${0}
    ${return_code}=    Libfuzzer Test    payload_parser    ${time}
    Should Be Equal    ${return_code}    ${0}
    ${return_code}=    Libfuzzer Test    secure_boot_cfv    ${time}
    Should Be Equal    ${return_code}    ${0}
    ${return_code}=    Libfuzzer Test    secure_boot_payload    ${time}
    Should Be Equal    ${return_code}    ${0}