import androidx.compose.desktop.ui.tooling.preview.Preview
import androidx.compose.foundation.layout.*
import androidx.compose.material.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Window
import androidx.compose.ui.window.application
import org.graphstream.ui.view.Viewer
import java.io.File
import javax.swing.JFileChooser

@Composable
@Preview
fun app() {
    var filePath by remember { mutableStateOf<String?>(null) }
    var graphViewer by remember { mutableStateOf<Viewer?>(null) }
    var totalCableLength by remember { mutableStateOf<Int?>(null) }

    Column(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Button(onClick = {
            val fileChooser = JFileChooser()
            val result = fileChooser.showOpenDialog(null)
            if (result == JFileChooser.APPROVE_OPTION) {
                val selectedFile = fileChooser.selectedFile
                filePath = selectedFile.absolutePath
                val graphProcessor = GraphProcessor()
                val (graph, totalSum) = graphProcessor.processFile(selectedFile)
                graphViewer = graph.display()
                totalCableLength = totalSum
            }
        }) {
            Text("Select File")
        }

        Spacer(modifier = Modifier.height(16.dp))

        filePath?.let {
            Text("Selected File: $it")
        }

        Spacer(modifier = Modifier.height(16.dp))

        totalCableLength?.let {
            Text("Total Cable Length: $it")
        }
    }
}

fun main() = application {
    System.setProperty("org.graphstream.ui", "swing")
    Window(onCloseRequest = ::exitApplication) {
        app()
    }
}