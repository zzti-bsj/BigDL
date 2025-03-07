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

package com.intel.analytics.bigdl.dllib.feature.transform.vision.image.augmentation

import com.intel.analytics.bigdl.dllib.feature.transform.vision.image.{FeatureTransformer, ImageFeature}
import com.intel.analytics.bigdl.dllib.utils.Log4Error
import org.opencv.core
import org.opencv.core.Mat

/**
 * Fill part of image with certain pixel value
 *
 * @param startX start x ratio
 * @param startY start y ratio
 * @param endX end x ratio
 * @param endY end y ratio
 * @param value filling value
 */
class Filler(startX: Float, startY: Float, endX: Float, endY: Float, value: Int = 255)
  extends FeatureTransformer {

  Log4Error.invalidInputError(startX >= 0 && startX <= 1, s"$startX should be in the range [0, 1]")
  Log4Error.invalidInputError(startY >= 0 && startY <= 1, s"$startY should be in the range [0, 1]")
  Log4Error.invalidInputError(endX >= 0 && endX <= 1, s"$endX should be in the range [0, 1]")
  Log4Error.invalidInputError(endY >= 0 && endY <= 1, s"$endY should be in the range [0, 1]")
  Log4Error.invalidInputError(endX > startX, s"$endX should be greater than $startX")
  Log4Error.invalidInputError(endY > startY, s"$endY should be greater than $startY")

  override def transformMat(feature: ImageFeature): Unit = {
    var fillMat: Mat = null
    var submat: Mat = null
    try {
      val mat = feature.opencvMat()
      val x1 = (startX * mat.cols()).ceil.toInt
      val x2 = (endX * mat.cols()).ceil.toInt
      val y1 = (startY * mat.rows()).ceil.toInt
      val y2 = (endY * mat.rows()).ceil.toInt
      fillMat = new core.Mat(y2 - y1, x2 - x1, mat.`type`(), new core.Scalar(value, value, value))
      submat = mat.submat(y1, y2, x1, x2)
      fillMat.copyTo(submat)
    } finally {
      if (null != fillMat) fillMat.release()
      if (null != submat) submat.release()
    }
  }
}

object Filler {
  def apply(startX: Float, startY: Float, endX: Float, endY: Float, value: Int = 255): Filler
  = new Filler(startX, startY, endX, endY, value)
}

