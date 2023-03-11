import java.util.*;
import java.util.function.*;

class Javaso {
    static int getSize(String[] args) {
        if (args.length < 1) {
            return 1000;
        }
        return Integer.parseInt(args[0]);
    }

    static long hoge(int[] d) {
        long sum = 0;
        for (int c = 0; c < d.length; ++c) {
            int v = d[c];
            if (128 <= v) {
                sum += v;
            }
        }
        return sum;
    }

    static long hogeo(int[] d) {
        long sum = 0;
        for (int c = 0; c < d.length; ++c) {
            int v = d[c];
            sum += (128 <= v ? 0xff : 0) & v;
        }
        return sum;
    }

    static long fuga(int[] d) {
        long sum = 0;
        for (int v : d) {
            if (128 <= v) {
                sum += v;
            }
        }
        return sum;
    }

    static void measure(
            String name,
            int[] data,
            Function<int[], Long> f) {
        long sum = 0;
        long t0 = System.nanoTime();
        for (int i = 0; i < 1000; ++i) {
            sum += f.apply(data);
        }
        long duration = System.nanoTime() - t0;
        double durMS = duration * 1e-6;
        System.out.printf("    %-6s: duration=%7.2fms  sum=%d\n", name, durMS, sum);

    }

    static int[] makeData(String[] args) {
        int[] data = new int[getSize(args)];
        for (int i = 0; i < data.length; ++i) {
            data[i] = i & 255;
        }
        return data;
    }

    static int[] shuffle(int[] d) {
        Random rand = new Random();
        for (int i = 1; i < d.length; ++i) {
            int j = rand.nextInt(i + 1);
            int t = d[i];
            d[i] = d[j];
            d[j] = t;
        }
        return d;
    }

    static void runtest(int[] data ){
        data = shuffle(data);
        System.out.println("  shuffled");
        measure("hoge", data, d -> hoge(d));
        measure("hogeo", data, d -> hogeo(d));
        measure("fuga", data, d -> fuga(d));
        Arrays.sort(data);
        System.out.println("  sorted");
        measure("hoge", data, d -> hoge(d));
        measure("hogeo", data, d -> hogeo(d));
        measure("fuga", data, d -> fuga(d));
    }

    public static void main(String[] args) {
        int[] data = makeData(args);
        for( int i=0 ; i<10000 ; ++i ){
            System.out.printf("i=%d\n", i);
            runtest(data);
        }
    }
}