package wangzaiyu.com.Utils;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.security.ProtectionDomain;

public class PythonExecutor {

    public static String runPythonScript(String scriptPath, String... args) throws Exception {
        // 构造命令（假设系统已配置Python环境变量）
        String[] command = new String[args.length + 2];
        command[0] = "python";  // 或 "python3"
        command[1] = scriptPath;
        System.arraycopy(args, 0, command, 2, args.length);

        // 启动进程
        ProcessBuilder pb = new ProcessBuilder(command);
        pb.redirectErrorStream(true);  // 合并错误流到输出流
        Process process = pb.start();

        // 读取输出
        StringBuilder output = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(process.getInputStream()))) {
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }
        }

        // 等待进程结束
        int exitCode = process.waitFor();
        if (exitCode != 0) {
            throw new RuntimeException("Python脚本执行失败，退出码: " + exitCode);
        }

        return output.toString();


    }

    public static void main(String[] args) throws Exception {
        String scriptPath = "D:\\pythonProject\\Server\\Config\\config.py";
        String output = PythonExecutor.runPythonScript(scriptPath);

    }
}