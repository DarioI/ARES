# This file is part of DroidSec.
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
    "instance-of": "Store in the given destination register 1 if the indicated reference is an instance of the given type, or 0 if not."


}
