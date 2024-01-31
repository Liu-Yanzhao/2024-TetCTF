# flip

* Category: CRYPTO

* Author: ndh

## Description:

* You are allowed to inject a software fault.

* Server: nc 139.162.24.230 31339

* Material: `flip.zip`

## Analysing source code

We get a few files of code, one called `main.py` and `encrypt`. 

And we look at `main.py`, we see there is one main function that is being called

In the first line, a key is randomly generated with `os.urandom()` which is impossible to crack.

```python
key = os.urandom(16)
```

Then the the program open the encrypt file and write its content into the variable content.

```python
with open("encrypt", "rb") as f:
    content = bytearray(f.read())
```

Now an input is taken in and a few checks were made.

```python
try:
    plaintext_hex, i_str, j_str = input().split()
    pt = bytes.fromhex(plaintext_hex)
    assert len(pt) == 16
    i = int(i_str)
    print(len(content))
    assert 0 <= i < len(content)
    j = int(j_str)
    assert 0 <= j < 8
except Exception as err:
    print(err, file=sys.stderr)
    ban_client()
    return
```

From the first line we we can see the input expects 3 inputs separated with a line, else it raises an ValueError and then exit the function.

The, it checks if the the byte format of `plaintext_hex` was length 16. Then afterwards it expects 2 integer values, the first one is more than or equal to 0 and less than the length of the content variable shown above. And the second variable has to be more than or equal to 0 and less than eight (the length of one byte).

If any of these checks fail, the `assert` keyword raises an AssertionError and quits the program. 

Then, the content is changed by inserting in the randomly generated key and the input. And weirdly, the lsat line flips the bit of the value of the content index i on the jth bit... thats interesting...

```python
# update key, plaintext, and inject the fault
content[OFFSET_KEY:OFFSET_KEY + 16] = key
content[OFFSET_PLAINTEXT:OFFSET_PLAINTEXT + 16] = pt
content[i] ^= (1 << j)
```

Then, a temporary file is created and the content is written to it. The program gave that file permissions to run iteself. Pretty simple.

```python
tmpfile = tempfile.NamedTemporaryFile(delete=True)
with open(tmpfile.name, "wb") as f:
    f.write(content)
os.chmod(tmpfile.name, 0o775)
tmpfile.file.close()
```

Then the file is run and its output is printed out to the console. Else if there were some error, the client will be banned amd the code will exit. 

```python
try:
    ciphertext = subprocess.check_output(tmpfile.name, timeout=1.0)
    print(ciphertext.hex())
except Exception as err:
    print(err, file=sys.stderr)
    ban_client()
    return
```

Finally, the most important part of the program is this part. This part takes in a second input and checks them against its own key. If its correct, flag.txt is read and printed out. 

```python
if bytes.fromhex(input()) == key:
    with open("secret/flag.txt") as f:
        print(f.read())
    from datetime import datetime
    print(datetime.now(), plaintext_hex, i, j, file=sys.stderr)
```

This means that we have to choose a i and j value that somehow leaks the key which we can enter and open flag.txt

## Analysing encrypt.c
The first line of code initialises the variables.

```c
uint8_t plaintext[16] = {0x20, 0x24};
uint8_t key[16] = {0x20, 0x24};
```

This is what we are overwriting in the `main.py`.

Then, we go into main() function.

```c
int main() {
    struct AES_ctx ctx;
    AES_init_ctx(&ctx, key);
    AES_ECB_encrypt(&ctx, plaintext);
    write(STDOUT_FILENO, plaintext, 16);
    return 0;
}
```

It encrypts the input that we give it and prints it out. This is where the vulnerability lie.

Honestly, I would not have been able to spot the vulnerability withouth flipv2 came out. lets look at the difference between flip v1 and flip v2

```python
OFFSET_PLAINTEXT = 0x4010
OFFSET_KEY = 0x4020
OFFSET_MAIN_START = 0x1169 #Change
OFFSET_MAIN_END = 0x11ed #Change

...

try:
    plaintext_hex, i_str, j_str = input().split()
    pt = bytes.fromhex(plaintext_hex)
    assert len(pt) == 16
    i = int(i_str)
    assert 0 <= i < len(content)
    assert not OFFSET_MAIN_START <= i < OFFSET_MAIN_END #Change
    j = int(j_str)
    assert 0 <= j < 8
except Exception as err:
    print(err, file=sys.stderr)
    ban_client()
    return
```

It seems like the program restricts us from flipping bytes at locations more than or equal to 0x1169 and 0x11ed.

Thats when I realised that we could change the number 16 on line of code below to print more than it needed to. Moreover, the key variable is right next to the plaintext, hence the flag will be leaked this way. 

```c
write(STDOUT_FILENO, plaintext, 16);
```

I just brute forced it and tried every single combination and seeing the response. I will know I reached the correct number when the output suddenly outputs something thats longer than 32 characters. (AES algorithm outputs an 32 character encrypted text from an plaintext with a length 0 to 32 character long).

```
41414141414141414141414141414141 4457 1
41414141414141414141414141414141 4458 1
41414141414141414141414141414141 4459 1 d11e0f993fd793a758bbfcb294dfff0a
41414141414141414141414141414141 4460 1 6391700ad7296146c617424383c5b3f6
41414141414141414141414141414141 4461 1 f3ad995deb798414eb47a9ed18e25974
41414141414141414141414141414141 4462 1 ddff06f2ae35eecb4a600fa29712fb82
41414141414141414141414141414141 4463 1
41414141414141414141414141414141 4464 1
41414141414141414141414141414141 4465 1 8f20fe37262ae5787356f66647d669c2
41414141414141414141414141414141 4466 1
41414141414141414141414141414141 4467 1
41414141414141414141414141414141 4468 1 d3238305a202bab2045a559c273ba077
41414141414141414141414141414141 4469 1 32f3c84bb433b5fb89561933366ed446
41414141414141414141414141414141 4470 1 67ddbd154ad6137f280f0526a77637f6
41414141414141414141414141414141 4471 1
41414141414141414141414141414141 4472 1
41414141414141414141414141414141 4473 1 200ee363bc160628fecac7b8443907f3
41414141414141414141414141414141 4474 1 6b4d7b62d8b8e6e35f64a945f051209e
41414141414141414141414141414141 4475 1
41414141414141414141414141414141 4476 1
41414141414141414141414141414141 4477 1
41414141414141414141414141414141 4478 1
41414141414141414141414141414141 4479 1
41414141414141414141414141414141 4480 1
41414141414141414141414141414141 4481 1 f08c98fc807b6463830234c0a9d5ba68
41414141414141414141414141414141 4482 1
41414141414141414141414141414141 4483 1
41414141414141414141414141414141 4484 1
41414141414141414141414141414141 4485 1 8b6a9bf7c1d6dfb0fe0cdffe390b2924
41414141414141414141414141414141 4486 1 d8bd311782feaac7e1e7cd696dfdeaab
41414141414141414141414141414141 4487 1 a1e197a2d14c5f34c0038dd9b8943a66
41414141414141414141414141414141 4488 1
41414141414141414141414141414141 4489 1
41414141414141414141414141414141 4490 1 c51308b26fc7a424fc1c866b19bc841a
41414141414141414141414141414141 4491 1 f81a78ac1338d1347cc04e83560d73a8
41414141414141414141414141414141 4492 1 b34a476d692a6a81c0ee6e5af849ab4f
41414141414141414141414141414141 4493 1
41414141414141414141414141414141 4494 1 71fcdf894f1657bb476ae907458b4cbf
41414141414141414141414141414141 4495 1
41414141414141414141414141414141 4496 1
41414141414141414141414141414141 4497 1 f62c366724ab7b59bf8eff3b338e7253
41414141414141414141414141414141 4498 1 c7336d2916e814029822e7a1de9d5c99
41414141414141414141414141414141 4499 1
41414141414141414141414141414141 4500 1
41414141414141414141414141414141 4501 1 af3f363b0b03ad2ba9c6cc4dadc3d403
41414141414141414141414141414141 4502 1 623bb5bb559e98b6f33c9927beb4e8c9
41414141414141414141414141414141 4503 1
41414141414141414141414141414141 4504 1 f7660738df1739d7704449eea6e1660a
41414141414141414141414141414141 4505 1
41414141414141414141414141414141 4506 1
41414141414141414141414141414141 4507 1
41414141414141414141414141414141 4508 1
41414141414141414141414141414141 4509 1
41414141414141414141414141414141 4510 1
41414141414141414141414141414141 4511 1
41414141414141414141414141414141 4512 1 5064f58a7769b3d218b4bb3f01d24835
41414141414141414141414141414141 4513 1
41414141414141414141414141414141 4514 1 e5213a2cc6c75fbedb7a54a06740e38e
41414141414141414141414141414141 4515 1 26c8a2bb8fc78209eb2e97abe72225b4
41414141414141414141414141414141 4516 1 2ff091400761e573e2966533bb51f607
41414141414141414141414141414141 4517 1 6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d6d
41414141414141414141414141414141 4518 1
41414141414141414141414141414141 4519 1 dcc2e00330ab16da6e3a5dfe4f7c1218
41414141414141414141414141414141 4520 1
41414141414141414141414141414141 4521 1
41414141414141414141414141414141 4522 1 44479bccfbd3ba8e0ca868dd37594141
41414141414141414141414141414141 4523 1
41414141414141414141414141414141 4524 1
41414141414141414141414141414141 4525 1
41414141414141414141414141414141 4526 1 b04de7928bc5fa1bf0c5f3bf7f8c41a3
41414141414141414141414141414141 4527 1
41414141414141414141414141414141 4528 1
41414141414141414141414141414141 4529 1 8cc14c317a618331b267d6a8383e1b6b
41414141414141414141414141414141 4530 1 e22e636bc1022661a482d4c1ddeac637
41414141414141414141414141414141 4531 1
41414141414141414141414141414141 4532 1
41414141414141414141414141414141 4533 1
41414141414141414141414141414141 4534 1
41414141414141414141414141414141 4535 1
41414141414141414141414141414141 4536 1
41414141414141414141414141414141 4537 1 0b644162cf43c1603d231eee24c55448a294784de7c5feae2ccec9396308005700000000000000000000000000000000000000000000000000000000000000000000000000000000
41414141414141414141414141414141 4538 1 745db492f436525d36b2aaabff3b993a09d8
41414141414141414141414141414141 4538 1 e9723ba7b691bcf1cda12f825c3f7c60 2214d62f259f3a82dc92d9880455dfd200000000000000000000000000000000
41414141414141414141414141414141 4539 1 389800f0434782470045a2fd220a81dfb2e2373026a036079218b41e25c3e54a00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
41414141414141414141414141414141 4540 1 "\n"
41414141414141414141414141414141 4541 1 "\n"
41414141414141414141414141414141 4542 1 75f6ae480fc58262808ab003ac1a50bc
41414141414141414141414141414141 4543 1 a44b3e062479ddac1d9e0ba7a3fc0c7e
41414141414141414141414141414141 4544 1
41414141414141414141414141414141 4545 1 00005c8a99680321ce4fe4fa03342372
41414141414141414141414141414141 4546 1 1a00000000000000b84d000000000000
41414141414141414141414141414141 4547 1 "\n"
41414141414141414141414141414141 4548 1 "\n"
41414141414141414141414141414141 4549 1 b66a8aca7cfc64ebf7c5094a26c8cf0b
41414141414141414141414141414141 4550 1 d92b4c5777fb349510d07bc6d330df92
41414141414141414141414141414141 4551 1 22fd9d5b6b31e600f919a61bdc0f41b8
41414141414141414141414141414141 4552 1
41414141414141414141414141414141 4553 1 "\n"
41414141414141414141414141414141 4554 1 "\n"
41414141414141414141414141414141 4555 1 "\n"
41414141414141414141414141414141 4556 1 "\n"
41414141414141414141414141414141 4557 1
41414141414141414141414141414141 4558 1 3473ad56cb6f5d7f8d4745b0c054fb9a
41414141414141414141414141414141 4559 1
41414141414141414141414141414141 4560 1
41414141414141414141414141414141 4561 1
41414141414141414141414141414141 4562 1
41414141414141414141414141414141 4563 1
41414141414141414141414141414141 4564 1 ed8e86b8fd01a6ca75ff722c88c5baaf
41414141414141414141414141414141 4565 1 27bf17025514b894a92f67364a600904
41414141414141414141414141414141 4566 1 58bee445f42d3020d492a15e4b2c4791
41414141414141414141414141414141 4567 1 e87d9a8019b3818dec85d4788261ab07
41414141414141414141414141414141 4568 1
41414141414141414141414141414141 4569 1
41414141414141414141414141414141 4570 1
41414141414141414141414141414141 4571 1
41414141414141414141414141414141 4572 1 3d2b549969ec2c4b8b4cff0f0644467e
41414141414141414141414141414141 4573 1 515283579fa863dc19a7ccfcc2c83b77
41414141414141414141414141414141 4574 1
41414141414141414141414141414141 4575 1
41414141414141414141414141414141 4576 1
41414141414141414141414141414141 4577 1
41414141414141414141414141414141 4578 1
41414141414141414141414141414141 4579 1
41414141414141414141414141414141 4580 1 f8fd2e3878dc32d7c63fb2d35835b460
41414141414141414141414141414141 4581 1
41414141414141414141414141414141 4582 1 0a57c14d22103000a4ebfb66d0130287
41414141414141414141414141414141 4583 1 c9be2d1b6a3ba273f44a6df94ccbf95d
41414141414141414141414141414141 4584 1 7752403d5e0a94efbefd0565a47199ce
41414141414141414141414141414141 4585 1 eb0b8982eea2c4f9896d43669a3f78f2
41414141414141414141414141414141 4586 1 35edf4bc47d0ee904e519ba448d82922
41414141414141414141414141414141 4587 1
41414141414141414141414141414141 4588 1
```

We can see that this combination created a larger output

`41414141414141414141414141414141 4538 1 `

We changed it to 

`41414141414141414141414141414141 4538 5` 

since 16 is 0b010000, by fliping the 5th byte, we get 0b110000 which is 48 charcters. Hence we will be expecting 96 hexadecimal charcters:

`e9723ba7b691bcf1cda12f825c3f7c602214d62f259f3a82dc92d9880455dfd200000000000000000000000000000000`

Remeber how each key is 32 hexadecimal characters long and the plaintext is also 32 hexadecimal characters, and we can slice the output string out to give us:

`e9723ba7b691bcf1cda12f825c3f7c60`\
`2214d62f259f3a82dc92d9880455dfd2`\
`00000000000000000000000000000000`

And since we know that the first line is our encrypted text, that leaves the second value to be the key!

And... if input that, we get the flag!

Flag: `TetCTF{fr0m_0n3_b1t_fl1pp3d_t0_full_k3y_r3c0v3ry}`