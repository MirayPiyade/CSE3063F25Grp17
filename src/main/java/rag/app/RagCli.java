package rag.app;

import rag.config.Config;

import rag.config.ConfigLoader;

import java.io.Console;
import java.util.Scanner;

public class RagCli {
    public static void main(String[] args) throws Exception {

        String configPath = extractArg(args, "--config");
        String cliQuestion = extractArg(args, "--q");
        String cliReranker = extractArg(args, "--reranker");

        Config baseConfig = ConfigLoader.load(configPath);
        String question = cliQuestion != null ? cliQuestion : baseConfig.getQuestion();
        if (question == null || question.isBlank()) {
            question = promptQuestion();
        }

        Config effectiveConfig = baseConfig.withQuestion(question);
        if (cliReranker != null && !cliReranker.isBlank()) {
            effectiveConfig = effectiveConfig.withRerankerType(cliReranker);
        }
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

    private static String extractArg(String[] args, String key) {
        if (args == null) return null;
        for (int i = 0; i < args.length; i++) {
            if (key.equals(args[i]) && i + 1 < args.length) {
                return args[i + 1];
            }
        }
        return null;
    }
}
