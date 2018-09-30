
// package Geo_processing
import org.nd4j.linalg.factory.Nd4j
import org.nd4j.linalg.api.ndarray.INDArray
import org.deeplearning4j.nn.modelimport.keras.KerasModelImport
import org.deeplearning4j.nn.graph.ComputationGraph
import scala.collection.JavaConverters._
// import org.deeplearning4j.embeddings.loader.WordVectorSerializer
import scala.collection.mutable.ListBuffer
import scala.io.Source
// import scala.reflect.ClassTag

object geo_2{
  def manOf[T: Manifest](t: T): Manifest[T] = manifest[T]

  def one_hot_vec(value:Int, max_value:Int) : Array[Int] = {
   var one_hot_representation = Array[Int](max_value)
   println("the one hot rep is: ", one_hot_representation.toString)
   return one_hot_representation
  }

  def main(args: Array[String]): Unit = {
    var case2Idx =  collection.mutable.Map("numeric" -> 0, "allLower"-> 1, "allUpper"-> 2, "initialUpper"-> 3, "other"-> 4, "mainly_numeric"-> 5,
      "contains_digit"-> 6, "PADDING_TOKEN"-> 7)


    var char2Idx = collection.mutable.Map("PADDING"-> 0.toFloat, "UNKNOWN"-> 1.toFloat)
    var counter1 = 2
    for (c <- "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,-_()[]{}!?:;#'\"/\\%$`&=*+@^~|".toList) {
      char2Idx += (c.toString->counter1.toFloat)
      counter1 += 1
    }

    val r = scala.util.Random
    val vector1 = for (i <- 0 to r.nextInt(300)) yield (i * r.nextFloat) // initializing the random vector
    println(vector1.toString())
    var word2Idx =  collection.mutable.Map("PADDING_TOKEN" -> 0.toFloat, "UNKNOWN_TOKEN" -> 1.toFloat)
    var word2Idx12 =  collection.mutable.Map("UNKNOWN_TOKEN" -> vector1)

    var word_counter = 2
    val emb_filename = "/Users/vikasy/Glove_vectors/Glove.840B.300d.txt"
    val word2idx_file = "/Users/vikasy/SEM_5/RA/Xu_Ma_Hovy/word2idx_file.txt"

    // val wv = WordVectorSerializer.loadTxtVectors(new Nothing(emb_filename))
    // println(wv)


    // println(word2Idx12)

    for (line <- Source.fromFile(word2idx_file).getLines) {
      val words = line.split(" ")
      word2Idx += (words(0).toString -> words(1).toFloat)
      word_counter += 1
    }

    /*
    for (line <- Source.fromFile(emb_filename).getLines) {
      val words = line.split(" ")
      if (word2Idx.keySet.exists(_ == words(0).toString)) {
        word2Idx12 += (words(0).toString -> words.drop(1).map(_.toFloat).toIndexedSeq)
        word_counter += 1
      }
    }
    */


    // println(word2Idx12)


    val sentence = List("South", "Sudan", "is", "a", "country", "in", "African", "continent")

    // var word_vector = new ListBuffer[Array[Int]] // List()
    // var char_vector = new ListBuffer[Any] // List()
    var word_feature = new ListBuffer[Float]
    var char_indexes = new ListBuffer[Float]
    for (word <- sentence){
      val chars = word.toList


      if (word2Idx.keySet.exists(_ == word.toString)){
        word_feature += word2Idx(word.toString)
      }

      else {
        word_feature += word2Idx("UNKNOWN_TOKEN")
      }



      for (char1 <- chars){

        if (char2Idx.keySet.exists(_ == char1.toString)){
          char_indexes += char2Idx(char1.toString)
        }

        else {
          char_indexes += char2Idx("UNKNOWN")
        }
      }
      while (char_indexes.length<52){  //padding character sequence
        char_indexes+=0.toFloat
      }

      // word_char_feature += char_indexes.toList
      // new_sentence += word_char_feature.toList
      // char_vector += char_indexes.toArray
      // word_vector += word_feature.toArray

    }
   println("length of feature vector is: ", word_feature.length)
   println(word_feature.toString())

    // one_hot_vec(5,10)  // Not required
    // conversion of input data to required DL4J NN library starts here
     val word_input = Nd4j.create(word_feature.toArray)  // asJava
     // println(word_input.toString)
     // val word_input = word_feature.asNDArray(word_feature.length,1) // asJava
     val char_input = Nd4j.create(char_indexes.toArray)
    println(char_input.toString)
//    modelPath = "model2.h5" // change this to be given as an argument by the user - same as Egoitz
//
//    // private val network: ComputationGraph = KerasModelImport.importKerasModelAndWeights(modelPath, false)
//
//    network.setInput(0, word_input)
//    network.setInput(1, char_input)
//    val results = network.feedForward()  // ask Egoitz, what to replace here.

  }


  //  def create_matrices( sentence1:List[(String, List[String])] ) : List[Any] = {
  //    var new_sent1 = new ListBuffer[Any] // List()
  //    for (duplets <- sentence1) {
  //      println(duplets)
  //      new_sent1+=duplets(0)
  //
  //    }
  //
  //    return new_sent1.toList
  //  }




}


