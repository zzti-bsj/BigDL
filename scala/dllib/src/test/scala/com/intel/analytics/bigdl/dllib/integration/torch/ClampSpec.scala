/*
 * Copyright 2016 The BigDL Authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.intel.analytics.bigdl.dllib.integration.torch

import com.intel.analytics.bigdl.dllib.nn.Clamp
import com.intel.analytics.bigdl.dllib.tensor.Tensor
import com.intel.analytics.bigdl.dllib.utils.TestUtils

import scala.math._

@com.intel.analytics.bigdl.tags.Serial
class ClampSpec extends TorchSpec {
    "A Clamp Module " should "generate correct output and grad" in {
    torchCheck()
    val module = new Clamp[Double](-10, 10)
    val input = Tensor[Double](2, 2, 2)
    input(Array(1, 1, 1)) = -0.97008799016476
    input(Array(1, 1, 2)) = -0.89318234380335
    input(Array(1, 2, 1)) = -0.65073125436902
    input(Array(1, 2, 2)) = -0.35406025126576
    input(Array(2, 1, 1)) = -1.0360766677186
    input(Array(2, 1, 2)) = 1.173689913936
    input(Array(2, 2, 1)) = 1.6776262558997
    input(Array(2, 2, 2)) = -0.64814318157732
    val gradOutput = Tensor[Double](2, 2, 2)
    gradOutput(Array(1, 1, 1)) = 0.43442418193445
    gradOutput(Array(1, 1, 2)) = 0.97614445211366
    gradOutput(Array(1, 2, 1)) = 0.081252868985757
    gradOutput(Array(1, 2, 2)) = 0.24688877537847
    gradOutput(Array(2, 1, 1)) = 0.027903598966077
    gradOutput(Array(2, 1, 2)) = 0.0086153273005038
    gradOutput(Array(2, 2, 1)) = 0.053113180678338
    gradOutput(Array(2, 2, 2)) = 0.74842141871341

    val start = System.nanoTime()
    val output = module.forward(input)
    val gradInput = module.backward(input, gradOutput)
    val end = System.nanoTime()
    val scalaTime = end - start

    val code = "module = nn.Clamp(-10, 10)\n" +
      "output = module:forward(input)\n" +
      "gradInput = module:backward(input,gradOutput)"

    val (luaTime, torchResult) = TH.run(code, Map("input" -> input, "gradOutput" -> gradOutput),
      Array("output", "gradInput"))
    val luaOutput1 = torchResult("output").asInstanceOf[Tensor[Double]]
    val luaOutput2 = torchResult("gradInput").asInstanceOf[Tensor[Double]]

    luaOutput1.map(output, (v1, v2) => {
      TestUtils.conditionFailTest(abs(v1 - v2) == 0)
      v1
    })
    luaOutput2.map(gradInput, (v1, v2) => {
      TestUtils.conditionFailTest(abs(v1 - v2) == 0)
      v1
    })

    println("Test case : Clamp, Torch : " + luaTime + " s, Scala : " + scalaTime / 1e9 + " s")
  }

}
