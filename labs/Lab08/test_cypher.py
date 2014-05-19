#!/usr/bin/env python2.6

import sys, os, cypher,string


# Comment out each section to test your module:


test_str = "this, is*a TEST /string/ 1 [2] 3:"
test_str_expected = "this isa TEST string 1 2 3"

test_str_res = cypher.strip_invalid_characters(test_str)

if test_str_res != test_str_expected:
	print "strip_invalid_characters - ERROR"
else:
	print "strip_invalid_characters - OK"

print "Expected:", test_str_expected
print "Got:", test_str_res


# -----------------------------------------------------------------


test_pw = "$hello"
test_pw_expected = False
test_pw_res = cypher.is_valid_password(test_pw)
if test_pw_res != test_pw_expected:
	print "is_valid_password - ERROR"
else:
	print "is_valid_password - OK"


# -----------------------------------------------------------------


test_str_res = cypher.strip_invalid_characters(test_str)

if test_str_res != test_str_expected:
	print "strip_invalid_characters - ERROR"
else:
	print "strip_invalid_characters - OK"
print "Expected:", test_str_expected
print "Got:", test_str_res


# -----------------------------------------------------------------


password="goldfarb"
message="the dog ate my lab report"
expected_message="OKEc8DMa6WEcGNqB6EkJ9EUHO"
encrypted_message=cypher.vign_encrypt(message, password)

if encrypted_message != expected_message:
	print "vign_encrypt - ERROR"
else:
	print "vign_encrypt - OK"

print "Expected:", expected_message
print "Got:", encrypted_message

# -----------------------------------------------------------------


decrypted_message=cypher.vign_decrypt(encrypted_message, password)
if decrypted_message != message:
	print "vign_decrypt - ERROR"
else:
	print "vign_decrypt - OK"

print "Expected:", message
print "Got:", decrypted_message


sys.exit(0)
