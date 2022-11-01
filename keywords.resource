*** Settings ***
Documentation     This is a resource file, that can contain variables and keywords.
...               Keywords defined here can be used where this Keywords.resource in loaded.
Library           CustomLibrary.py


*** Keywords ***
Clone Source Code
    ${return_code}=    Clone    https://github.com/confidential-containers/td-shim.git    td-shim
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
    ${return_code}=    Afl Test    ${time}
    Should Be Equal    ${return_code}    ${0}

Libfuzzer
    [Arguments]    ${time}
    ${return_code}=    Libfuzzer Test    ${time}
    Should Be Equal    ${return_code}    ${0}