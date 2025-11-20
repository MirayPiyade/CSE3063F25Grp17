package rag.app;

import rag.config.Config;

import java.io.Console;
import java.util.Arrays;
import java.util.Scanner;

public class RagCli {
    public static void main(String[] args) throws Exception {

        if (args.length < 1) {
            System.out.println("Usage: java RagCli <config.yaml> [question]");
            return;
        }

        Config config = Config.load(args[0]);
        String question = args.length > 1
                ? String.join(" ", Arrays.copyOfRange(args, 1, args.length))
                : promptQuestion();

        if (question == null || question.isBlank()) {
            question = config.getQuestion();
        }

        if (question == null || question.isBlank()) {
            System.err.println("No question provided. Please enter a question to continue.");
            return;
        }

        Config effectiveConfig = config.withQuestion(question);
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
