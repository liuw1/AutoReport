*** Settings ***
Documentation     A test suite for td-shim validation.
...
...               Keywords are imported from the resource file
Resource          keywords.resource
Default Tags      positive

*** Test Cases ***
Clone Lasted TD-Shim Souce Code
    Clone Source Code
    Get Version

Build Final Binary With Boot-Kernel Support
    Build Final Binary    boot_kernel

Build Final Binary With PE Fromat TD Payload
    Build Final Binary    pe

Build Final Binary With ELF Fromat TD Payload
    Build Final Binary    elf

Build Final Binary with PE format test Payload
    Build Final Binary    pe_test

Run PE format test TD Payload
    Run Integration Test    1    2G    target/release/final-pe-test1.bin
    Run Integration Test    1    2G    target/release/final-pe-test2.bin
    Run Integration Test    2    4G    target/release/final-pe-test3.bin
    Run Integration Test    4    8G    target/release/final-pe-test4.bin
    Run Integration Test    8    16G    target/release/final-pe-test5.bin

Build Final Binary with ELF format test Payload
    Build Final Binary    elf_test

Run ELF format test TD Payload
    Run Integration Test    1    1G    target/release/final-elf-test1.bin
    Run Integration Test    1    2G    target/release/final-elf-test2.bin
    Run Integration Test    2    4G    target/release/final-elf-test3.bin
    Run Integration Test    4    8G    target/release/final-elf-test4.bin
    Run Integration Test    8    16G    target/release/final-elf-test5.bin

Build Final Binary with PE format payload for secure boot test
    Build Final Binary    pe_sb_test

Run Secure Boot test - PE format payload
    Run Integration Test    1    1G    target/release/final-pe-sb-normal.bin
    Run Integration Test    1    1G    target/release/final-pe-sb-mismatch-pubkey.bin
    Run Integration Test    1    1G    target/release/final-pe-sb-unsigned.bin

Build Final Binary with ELF format payload for secure boot test
    Build Final Binary    elf_sb_test

Run Secure Boot test - ELF format payload
    Run Integration Test    1    1G    target/release/final-elf-sb-normal.bin
    Run Integration Test    1    1G    target/release/final-elf-sb-mismatch-pubkey.bin
    Run Integration Test    1    1G    target/release/final-elf-sb-unsigned.bin

AFL Fuzzing
    Afl    10

Libfuzzer Fuzzing
    Libfuzzer    20