package rag.app;

import java.util.HashMap;
import java.util.Map;

public class StrategyRegistry {

    private static final Map<String, Class<?>> registry = new HashMap<>();

    public static void register(String key, Class<?> clazz) {
        registry.put(key, clazz);
    }

    public static Class<?> resolve(String key) {
        return registry.get(key);
    }
}
