# This file is part of ARES.
#
# Copyright (C) 2015, Dario Incalza <dario.incalza at gmail.com>
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'Dario Incalza <dario.incalza@gmail.com>'

TAINTED_PACKAGE_CREATE = 0
TAINTED_PACKAGE_CALL = 1

TAINTED_PACKAGE = {
   TAINTED_PACKAGE_CREATE : "C",
   TAINTED_PACKAGE_CALL : "M"
}

DEX_BYTECODE_SET = {
    "nop": "Waste cycles.",
    "move": "Move the contents of one non-object register to another.",
    "move-wide": "Move the contents of one register-pair to another.\nNote: It is legal to move from vN to either vN-1 or vN+1, so implementations must arrange for both halves of a register pair to be read before anything is written.",
    "move-object": "Move the contents of one object-bearing register to another.",
    "move-result": "Move the single-word non-object result of the most recent invoke-kind into the indicated register. This must be done as the instruction immediately after an invoke-kind whose (single-word, non-object) result is not to be ignored; anywhere else is invalid.",
    "move-result-wide": "Move the double-word result of the most recent invoke-kind into the indicated register pair. This must be done as the instruction immediately after an invoke-kind whose (double-word) result is not to be ignored; anywhere else is invalid.",
    "move-result-object": "Move the object result of the most recent invoke-kind into the indicated register. This must be done as the instruction immediately after an invoke-kind or filled-new-array whose (object) result is not to be ignored; anywhere else is invalid.",
    "move-exception": "Save a just-caught exception into the given register. This must be the first instruction of any exception handler whose caught exception is not to be ignored, and this instruction must only ever occur as the first instruction of an exception handler; anywhere else is invalid.",
    "return-void": "Return from a void method.",
    "return": "Return from a single-width (32-bit) non-object value-returning method.",
    "return-wide": "Return from a double-width (64-bit) value-returning method.",
    "return-object": "Return from an object-returning method.",
    "const": "Move the given literal value (sign-extended to 32 bits) into the specified register.",
    "const-wide": "Move the given literal value (sign-extended to 64 bits) into the specified register-pair.",
    "const-string": "Move a reference to the string specified by the given index into the specified register.",
    "const-class": "Move a reference to the class specified by the given index into the specified register. In the case where the indicated type is primitive, this will store a reference to the primitive type's degenerate class.",
    "monitor-enter": "Acquire the monitor for the indicated object.",
    "monitor-exit": "Release the monitor for the indicated object.\nNote: If this instruction needs to throw an exception, it must do so as if the pc has already advanced past the instruction. It may be useful to think of this as the instruction successfully executing (in a sense), and the exception getting thrown after the instruction but before the next one gets a chance to run. This definition makes it possible for a method to use a monitor cleanup catch-all (e.g., finally) block as the monitor cleanup for that block itself, as a way to handle the arbitrary exceptions that might get thrown due to the historical implementation of Thread.stop(), while still managing to have proper monitor hygiene.",
    "check-cast": "Throw a ClassCastException if the reference in the given register cannot be cast to the indicated type.",
    "instance-of": "Store in the given destination register 1 if the indicated reference is an instance of the given type, or 0 if not.",
    "array-length": "Store in the given destination register the length of the indicated array, in entries",
    "new-instance": "Construct a new instance of the indicated type, storing a reference to it in the destination. The type must refer to a non-array class.",
    "new-array" : "Construct a new array of the indicated type and size. The type must be an array type.",
    "filled-new-array" : "Construct an array of the given type and size, filling it with the supplied contents. The type must be an array type. The array's contents must be single-word (that is, no arrays of long or double, but reference types are acceptable). The constructed instance is stored as a 'result' in the same way that the method invocation instructions store their results, so the constructed instance must be moved to a register with an immediately subsequent move-result-object instruction (if it is to be used).",
    "fill-array-data" : "Fill the given array with the indicated data. The reference must be to an array of primitives, and the data table must match it in type and must contain no more elements than will fit in the array. That is, the array may be larger than the table, and if so, only the initial elements of the array are set, ",
    "throw" : "Throw the indicated exception.",
    "goto" : "Unconditionally jump to the indicated instruction.\nNote: The branch offset must not be 0. (A spin loop may be legally constructed either with goto/32 or by including a nop as a target before the branch.)",
    "packed-switch" : "Jump to a new instruction based on the value in the given register, using a table of offsets corresponding to each value in a particular integral range, or fall through to the next instruction if there is no match.",
    "sparse-switch" : "Jump to a new instruction based on the value in the given register, using an ordered table of value-offset pairs, or fall through to the next instruction if there is no match.",
    "if-eq" : "Branch to the given destination if the given two registers' values compare as specified.",
    "if-ne" : "Branch to the given destination if the given two registers' values compare as specified.",
    "if-lt" : "Branch to the given destination if the given two registers' values compare as specified.",
    "if-ge" : "Branch to the given destination if the given two registers' values compare as specified.",
    "if-gt" : "Branch to the given destination if the given two registers' values compare as specified.",
    "if-le" : "Branch to the given destination if the given two registers' values compare as specified.",
    "if-eqz" : "Branch to the given destination if the given register's value compares with 0 as specified.",
    "if-nez" : "Branch to the given destination if the given register's value compares with 0 as specified.",
    "if-ltz" : "Branch to the given destination if the given register's value compares with 0 as specified.",
    "if-gez" : "Branch to the given destination if the given register's value compares with 0 as specified.",
    "if-gtz" : "Branch to the given destination if the given register's value compares with 0 as specified.",
    "if-lez" : "Branch to the given destination if the given register's value compares with 0 as specified.",
    "aget"   : "Perform the identified array operation at the identified index of the given array, loading or storing into the value register.",
    "aget-wide":"Perform the identified array operation at the identified index of the given array, loading or storing into the value register.",
    "aget-object":"Perform the identified array operation at the identified index of the given array, loading or storing into the value register.",
    "aget-boolean":"Perform the identified array operation at the identified index of the given array, loading or storing into the value register.",
    "aget-byte":"Perform the identified array operation at the identified index of the given array, loading or storing into the value register.",
    "aget-char":"Perform the identified array operation at the identified index of the given array, loading or storing into the value register.",
    "aget-short":"Perform the identified array operation at the identified index of the given array, loading or storing into the value register.",
    "aput":"Perform the identified array operation at the identified index of the given array, loading or storing into the value register.",
    "aput-wide":"Perform the identified array operation at the identified index of the given array, loading or storing into the value register.",
    "aput-object":"Perform the identified array operation at the identified index of the given array, loading or storing into the value register.",
    "aput-boolean":"Perform the identified array operation at the identified index of the given array, loading or storing into the value register.",
    "aput-byte":"Perform the identified array operation at the identified index of the given array, loading or storing into the value register.",
    "aput-char":"Perform the identified array operation at the identified index of the given array, loading or storing into the value register.",
    "aput-short":"Perform the identified array operation at the identified index of the given array, loading or storing into the value register."
}
