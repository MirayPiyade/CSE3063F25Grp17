package rag.app;

import rag.config.Config;

import java.io.Console;
import java.util.Scanner;

public class RagCli {
    public static void main(String[] args) throws Exception {

        Config baseConfig = Config.defaultConfig();
        String question = promptQuestion();

        if (question == null || question.isBlank()) {
            System.err.println("No question provided. Please enter a question to continue.");
            return;
        }

        Config effectiveConfig = baseConfig.withQuestion(question);
        RagOrchestrator orchestrator = new RagOrchestrator(effectiveConfig);
        orchestrator.run();
    }

    private static String promptQuestion() {
        Console console = System.console();
        if (console != null) {
            return console.readLine("Question: ");
        }
        System.out.print("Question: ");
        Scanner scanner = new Scanner(System.in);
        return scanner.hasNextLine() ? scanner.nextLine() : null;
    }
}
